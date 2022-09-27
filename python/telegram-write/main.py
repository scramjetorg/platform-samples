from scramjet.streams import Stream
import requests

provides = {
   'provides': 'telegram-inbound',
   'contentType': 'text/plain'
}


def send_message(msg: str):
	url = f"https://api.telegram.org/bot{run.TOKEN}/sendMessage?chat_id={run.CHANNEL_ID}&text={msg}"
	requests.get(url).json()

async def run(context, input):
	config = context.config
	run.TOKEN = config['credentials']['token']
	run.CHANNEL_ID = config['credentials']['channel']
	
	return input.each(send_message)
