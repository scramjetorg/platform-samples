import asyncio
from scramjet.streams import Stream
import requests
import requests_async
import json
from shiftarray import ShiftArray

provides = {"provides": "pipe", "contentType": "text/plain"}

WAIT_TIME_ON_USER = 5
WAIT_TIME_ERROR = 3

class Auth0:
    def __init__(self, verified_url, users_url, api_url, request_data, stream):
        self.verified_url = verified_url
        self.users_url = users_url
        self.api_url = api_url
        self.request_data = request_data
        self.token_header = {
            "content-type": "application/json",
        }
        self.stream = stream

    def lookahead(self, iterable):
        it = iter(iterable)
        last = next(it)
        for val in it:
            yield last, True
            last = val
        yield last, False

    async def get_auth(self):
        last_verified = ""
        last_user = ""
        buffer_verified = ShiftArray()
        buffer_users = ShiftArray()
        response = requests.post(
            self.api_url, headers=self.token_header, data=self.request_data
        )
        token = json.loads(response.text)["access_token"]
        while True:
            headers = {"authorization": f"Bearer {token}"}
            verified =  await requests_async.get(self.verified_url, headers=headers)
            users = await requests_async.get(self.users_url, headers=headers)
            if verified.status_code != 200:
                await asyncio.sleep(WAIT_TIME_ERROR)
                response = requests.post(
                    self.api_url, headers=self.token_header, data=self.request_data
                )
                token = json.loads(response.text)["access_token"]
                continue
            verified = verified.json()
            users = users.json()
            if verified[-1]["email"] != last_verified:
                for result, has_more in self.lookahead(verified):
                    if not buffer_verified.contains(result["email"]):
                        self.stream.write(
                            result["email"] + " " + result["nickname"] + " auth0-newsletter"
                        )
                        buffer_verified.append(result["email"])
                    if not has_more:
                        last_verified = result["email"]

            if users[-1]["email"] != last_user:
                for result, has_more in self.lookahead(users):
                    if not buffer_users.contains(result["email"]):
                        self.stream.write(
                            result["email"] + " " + result["nickname"] + " auth0-user"
                        )
                        buffer_users.append(result["email"])
                    if not has_more:
                        last_user = result["email"]
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
        raise Exception(f"Config not loaded: {error}")

    asyncio.gather(
            Auth0(run.verified_url,run.users_url ,run.api_url, run.data, stream).get_auth(),
            return_exceptions=True,
        )
    return stream.map(lambda x: x + "\n")
