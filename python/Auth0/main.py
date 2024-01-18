import requests
import json
import enum
import asyncio
from shiftarray import ShiftArray
from scramjet.streams import Stream

provides = {"provides": "pipe", "contentType": "text/plain"}

WAIT_TIME_ON_USER = 5
WAIT_TIME_ERROR = 3

TOKEN_HEADER = {"content-type": "application/json"}

class TokenRefreshResult(enum.Enum):
    SUCCESS = 200
    FAILURE = 0


class Auth0:
    def __init__(self, verified_url, users_url, api_url, request_data, stream, logger):
        self.verified_url = verified_url
        self.users_url = users_url
        self.api_url = api_url
        self.token_payload = request_data
        self.stream = stream
        self.logger = logger

    def lookahead(self, iterable):
        it = iter(iterable)
        last = next(it)
        for val in it:
            yield last, True
            last = val
        yield last, False


    async def refresh_token(self):
        response = requests.post(
                    self.api_url, headers=TOKEN_HEADER, data=self.token_payload
                    )
        if response.status_code == TokenRefreshResult.SUCCESS.value:
            self.logger.info("Auth0: Token succesfully refreshed!")
            return TokenRefreshResult.SUCCESS.value, json.loads(response.text)["access_token"]
        
        self.logger.error("Auth0: Refreshing the token has failed!")
        return TokenRefreshResult.FAILURE.value, None
        

    async def get_auth(self):

        code, token = await self.refresh_token()

        if code != 200:
            raise Exception(f"Auth0: Refreshing the token has failed!")
        
        self.logger.info(f"Auth0: Succesfully initiated the token - code: {code}, token: {token}")

        last_verified = str()
        last_user = str()
        buffer_verified = ShiftArray()
        buffer_users = ShiftArray()

        while True:
            headers = {"authorization": f"Bearer {token}"}

            try:
                verified =  requests.get(self.verified_url, headers=headers)
                users = requests.get(self.users_url, headers=headers)
            except Exception as error:
                raise Exception(f"Auth0: Failed to make a request: {error}")
            
        
            if users.status_code != 200:
                await asyncio.sleep(WAIT_TIME_ERROR)
                self.logger.info("Auth0: Token's refresh was forced.")

                code, token = await self.refresh_token()
                continue

            verified = verified.json()
            users = users.json()


            if users[-1]["email"] != last_user:
                for result, has_more in self.lookahead(users):
                    if not buffer_users.contains(result["email"]):
                        self.logger.info(f"Auth0: New user registered in auth0: {result['email']}")
                        self.stream.write(
                            result["email"] + " " + result["nickname"] + " auth0-user"
                        )
                        buffer_users.append(result["email"])
                    if not has_more:
                        last_user = result["email"]
            
            if verified[-1]["email"] != last_verified:
                for result, has_more in self.lookahead(verified):
                    if not buffer_verified.contains(result["email"]):
                        self.logger.info(f"Auth0: User allowed the newsletter: {result['email']}")
                        self.stream.write(
                            result["email"] + " " + result["nickname"] + " auth0-newsletter"
                        )
                        buffer_verified.append(result["email"])
                    if not has_more:
                        last_verified = result["email"]
            await asyncio.sleep(WAIT_TIME_ON_USER)


async def run(context, input):
    config = context.config
    stream = Stream()

    try:
        run.verified_url = config["auth0_verified_url"]
        run.users_url = config["auth0_users_url"] 
        run.api_url = config["api_url"]
        run.data = json.dumps(config["request_data"])
    except Exception as error:
        raise Exception(f"Auth0: Config not loaded: {error}")

    asyncio.gather(
            Auth0(run.verified_url, run.users_url , run.api_url, run.data, stream, context.logger).get_auth(),
            return_exceptions=True,
        )
    return stream.map(lambda x: x + "\n")
