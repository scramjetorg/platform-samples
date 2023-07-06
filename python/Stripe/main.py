import requests
import stripe
import asyncio
from scramjet.streams import Stream

provides = {
    'provides': 'pipe',
    'contentType': 'text/plain'
}

class Stripe:
      def __init__(self,stream,stripe_api):
            self.stream = stream
            self.stripe_api = stripe_api
      
      def get_mail(self, user):
            return user['data']['object']['email']
      
      def get_fullname(self, user):
            mail = user['data']['object']['email']
            name = mail.split("@")
            name = name[0] + " stripe"
            return name
      
      async def get_event(self):
            await asyncio.sleep(3)
            compared = stripe.Event.list(type="customer.created")['data'][-1]

            self.stream.write(self.get_mail(compared)+ " " +self.get_fullname(compared))
            compared = compared['id']
            while True:
                  test = stripe.Event.list(type="customer.created", ending_before=compared, limit=3)['data']

                  for i in range(len(test)):
                        self.stream.write(self.get_mail(test[i]) + " " +self.get_fullname(test[i]))
                  if len(test) != 0:
                        compared = test[0]['id']
                  await asyncio.sleep(3)

async def run(context, input):
      stream = Stream()
      try:
            stripe.api_key = context.config['stripe_api']
            stripeReader = Stripe(stream, stripe.api_key)
      except Exception as error:
            raise Exception(f"Config not loaded: {error}")
            return
      asyncio.gather(stripeReader.get_event(), return_exceptions=True)
      return stream.map(lambda x : x + "\n")