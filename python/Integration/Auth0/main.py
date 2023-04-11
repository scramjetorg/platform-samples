import asyncio
from scramjet.streams import Stream
import requests
import stripe

url = "https://dev-scp.eu.auth0.com/api/v2/users?per_page=5&sort=created_at%3A1&fields=created_at%2Cupdated_at%2Cemail%2Cnickname&q=user_metadata.newsletter%3D%22true%22"

provides = {
    'provides': 'pipe',
    'contentType': 'text/plain'
}
def lookahead(iterable):
    it = iter(iterable)
    last = next(it)
    for val in it:
        yield last, True
        last = val
    yield last, False

async def get_auth(stream):
	headers = {'authorization' : run.auth}
	last = ""
	while True:
		users = requests.get(url, headers=headers).json()
		if users[-1]['email'] != last:
			for result, has_more in lookahead(users):
				stream.write(result['email'] +" "+result['nickname']+" auth0-user")
				if not has_more:
					last = result['email']
					
		await asyncio.sleep(5)
	

async def run(context, input):
	config = context.config
	stream = Stream()
	run.auth = config['auth']
	asyncio.gather(get_auth(stream), return_exceptions=True)
	return stream.map(lambda x : x + "\n")
