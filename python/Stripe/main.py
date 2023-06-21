import requests
import stripe
import asyncio
from scramjet.streams import Stream

provides = {
    'provides': 'pipe',
    'contentType': 'text/plain'
}


def get_mail(user):
	return user['data']['object']['email']
	
def get_fullname(user):
	mail = user['data']['object']['email']
	name = mail.split("@")
	name = name[0] + " stripe"
	return name

async def get_event(stream):
	await asyncio.sleep(3)
	compared = stripe.Event.list(type="customer.created")['data'][-1]
	tako = stripe.Event.list(type="customer.created")['data']

	stream.write(get_mail(compared)+ " " +get_fullname(compared))
	get_fullname(compared)
	compared = compared['id']
	while True:
		test = stripe.Event.list(type="customer.created", ending_before=compared, limit=3)['data']

		for i in range(len(test)):
			stream.write(get_mail(test[i]) + " " +get_fullname(test[i]))
		if len(test) != 0:
			compared = test[0]['id']
		await asyncio.sleep(3)
		

async def run(context, input):
	try:
		stripe.api_key = context.config['stripe_api']
	except Exception as error:
		raise Exception(f"Config not loaded: {error}")
		return
	stream = Stream()
	asyncio.gather(get_event(stream), return_exceptions=True)
	return stream.map(lambda x : x + "\n")
	
	
	
