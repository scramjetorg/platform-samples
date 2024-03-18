import requests
import json
import enum
import asyncio
from shiftarray import ShiftArray
from scramjet.streams import Stream



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
        self.logger.error(f"Auth0: {response.text}")
        return TokenRefreshResult.FAILURE.value, None
    

    async def process_users(self, last_user, users, buffer_users):
        for result, has_more in self.lookahead(users):
            if not buffer_users.contains(result["email"]):
                self.logger.info(f"Auth0: New user registered in auth0: {result['email']}")
                self.stream.write(
                    result["email"] + " " + result["nickname"] + " auth0-user"
                )
                buffer_users.append(result["email"])
            if not has_more:
                last_user = result["email"]
        return last_user

    async def process_verified(self, last_verified, verified, buffer_verified):
        for result, has_more in self.lookahead(verified):
            if not buffer_verified.contains(result["email"]):
                self.logger.info(f"Auth0: User allowed the newsletter: {result['email']}")
                self.stream.write(
                    result["email"] + " " + result["nickname"] + " auth0-newsletter"
                )
                self.logger.info(f"Auth0: User allowed the newsletter: {result['email']} wpiiiiisane")

                buffer_verified.append(result["email"])
            if not has_more:
                last_verified = result["email"]
        return last_verified
    


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
                self.logger.error(f"Auth0: {users.text}")

                code, token = await self.refresh_token()
                continue

            verified = verified.json()
            users = users.json()

            if users[-1]["email"] != last_user:
                last_user = await self.process_users(last_user, users, buffer_users)
            
            if verified[-1]["email"] != last_verified:
                last_verified = await self.process_verified(last_verified, verified, buffer_verified)


            await asyncio.sleep(WAIT_TIME_ON_USER)

