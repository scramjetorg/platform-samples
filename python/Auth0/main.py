import asyncio
from scramjet.streams import Stream
import requests
import json

class ShiftArray:
	def __init__(self):
		self.array = []

	def append(self, value):
		if len(self.array) == 5:
			self.array.pop(-1)
		self.array.append(value)

	def contains(self, value):
		return value in self.array

	def get_values(self):
		return self.array


def lookahead(iterable):
    it = iter(iterable)
    last = next(it)
    for val in it:
        yield last, True
        last = val
    yield last, False

provides = {
    'provides': 'pipe',
    'contentType': 'text/plain'
}

async def get_auth(stream):
	token_header = {'content-type': 'application/json',}
	last = ""
	buffer = ShiftArray()
	response = requests.post(run.api_url, headers=token_header, data=run.data)
	token = json.loads(response.text)['access_token']
	
	while True:
		headers = {'authorization' : f"Bearer {token}"}
		users = requests.get(run.query, headers=headers).json()
		
		if "error" in str(users):
			response = requests.post(run.api_url, headers=token_header, data=run.data)
			token = json.loads(response.text)['access_token']
			continue

		if users[-1]['email'] != last:
			for result, has_more in lookahead(users):
				if not buffer.contains(result['email']):
					stream.write(result['email'] +" "+result['nickname']+" auth0-user")
					buffer.append(result['email'])
				if not has_more:
					last = result['email']
		await asyncio.sleep(5) 

async def run(context, input):
	config = context.config
	stream = Stream()
	run.query = config['auth0_query_url']
	run.api_url = config['api_url']
	run.data = json.dumps(config['request_data'])
	asyncio.gather(get_auth(stream), return_exceptions=True)
	return stream.map(lambda x : x + '\n')