import asyncio
from scramjet.streams import Stream
import requests



provides = {
    'provides': 'telegram-outbound',
    'contentType': 'text/plain'
}

message = {
	"text": "text",
	"msg_id":"msg_id",
	"ch_id":"ch_id"
}

def message_update(message, result):
	message["text"] = result[-1]["channel_post"]["text"]
	message["msg_id"] = result[-1]['channel_post']["message_id"]
	message["ch_id"] = str(result[-1]['channel_post']['sender_chat']['id'])

async def get_updates(stream):
	url = f"https://api.telegram.org/bot{run.TOKEN}/getUpdates?chat_id={run.CHANNEL_ID}"
	msgid = 0
	while True:
		result = requests.get(url).json()['result']
		if result != []:
			message_update(message, result)
			if message["msg_id"] != msgid and message["ch_id"] == run.CHANNEL_ID:
				msgid = message["msg_id"]
				stream.write(message["text"])
		else:
			stream.write("No messages currently available")
		await asyncio.sleep(5)
		
		
	
async def run(context, input):
	config = context.config
	stream = Stream()
	run.TOKEN = config['credentials']['token']
	run.CHANNEL_ID = config['credentials']['channel']
	asyncio.gather(get_updates(stream), return_exceptions=True)
	return stream.map(lambda x : x + "\n")
