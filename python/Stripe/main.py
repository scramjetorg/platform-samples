import requests
import stripe
import asyncio
from scramjet.streams import Stream

EVENT_REFRESH_DELAY = 3

provides = {
    'provides': 'pipe',
    'contentType': 'text/plain'
}

class Stripe:
      def __init__(self, stream, stripe_api, logger):
            self.stream = stream
            self.stripe_api = stripe_api
            self.logger = logger
      
      def get_mail(self, user):
            return user['data']['object']['email']
      
      def get_fullname(self, user):
            mail = user['data']['object']['email']
            name = mail.split("@")
            name = name[0] + " stripe"
            return name
      
      async def get_event(self):
            compared = stripe.Event.list(type="customer.created")['data'][-1]

            self.logger.info(f"Stripe: New user in stripe {self.get_mail(compared)}")
            self.stream.write(self.get_mail(compared)+ " " + self.get_fullname(compared))

            compared = compared['id']

            while True:
                  events = stripe.Event.list(type="customer.created", ending_before=compared, limit=3)['data']
                  
                  for i in range(len(events)):
                        self.logger.info(f"Stripe: New user in stripe {self.get_mail(events[i])}")
                        self.stream.write(self.get_mail(events[i]) + " " + self.get_fullname(events[i]))
                  if len(events) != 0:
                        compared = events[0]['id']

                  await asyncio.sleep(EVENT_REFRESH_DELAY)

async def run(context, input):
      stream = Stream()
      try:
            stripe.api_key = context.config['stripe_api']
            stripeReader = Stripe(stream, stripe.api_key, context.logger)
      except Exception as error:
            raise Exception(f"Config not loaded: {error}")
            return
      asyncio.gather(stripeReader.get_event(), return_exceptions=True)
      return stream.map(lambda x : x + "\n")