import asyncio
from scramjet.streams import Stream
import requests
import sys



provides = {
    'provides': 'telegram-outbound',
    'contentType': 'text/plain'
}

async def get_updates(stream):
	temp = []
	url = f"https://api.telegram.org/bot{run.TOKEN}/getUpdates?chat_id={run.CHANNEL_ID}"
	while True:
		result = requests.get(url).json()['result']
		result = result[-1]["channel_post"]["text"]
		if result == "stop":
			sys.exit()
			return
		if result not in temp:
			temp.append(result)
			stream.write(result)
		await asyncio.sleep(5)
		
		
	
async def run(context, input):
	config = context.config
	stream = Stream()
	run.TOKEN = config['credentials']['token']
	run.CHANNEL_ID = config['credentials']['channel']
	asyncio.create_task(get_updates(stream))
	return stream.map(lambda x : x + "\n")
