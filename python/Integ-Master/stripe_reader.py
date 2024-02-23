import stripe
import asyncio
import enum
from scramjet.streams import Stream

EVENT_REFRESH_DELAY = 3
DELAY_ON_FAIL = 3

class EventRequestResult(enum.Enum):
    SUCCESS = 200
    FAILURE = 0

class Stripe:
      def __init__(self, stripe_api, stream, logger):
            self.stream = stream
            stripe.api_key = stripe_api
            self.logger = logger
            
      def get_mail(self, user):
            return user['data']['object']['email']
      
      def get_fullname(self, user):
            mail = user['data']['object']['email']
            name = mail.split("@")
            name = name[0] + " stripe"
            return name

      async def request_events(self, init = False, index = 0):
            if init:
                  try:
                        response = stripe.Event.list(type="customer.created")
                        data = response.get('data', [])
                        if not data:
                              return None, EventRequestResult.FAILURE.value
                        return data[-1], EventRequestResult.SUCCESS.value
                  except Exception as error:
                        return None, EventRequestResult.FAILURE.value
            
            try:
                  response = stripe.Event.list(type="customer.created", ending_before=index, limit=3)['data']
                  return response, EventRequestResult.SUCCESS.value
            except Exception as error:
                  return None, EventRequestResult.FAILURE.value
            

      
      async def get_event(self):
            compared, code = await self.request_events(True)

            if code != 200:
                  raise Exception(f"Stripe: Failed to init the request!")
            
            self.logger.info(f"Stripe: New user in stripe {self.get_mail(compared)}")
            self.stream.write(self.get_mail(compared)+ " " + self.get_fullname(compared))

            compared = compared['id']

            while True:
                  events, code = await self.request_events(index=compared)

                  if code != 200:
                        self.logger.info(f"Stripe: Failed to send the request!")
                        await asyncio.sleep(DELAY_ON_FAIL)
                        continue

                  
                  for i in range(len(events)):
                        self.logger.info(f"Stripe: New user in stripe {self.get_mail(events[i])}")
                        self.stream.write(self.get_mail(events[i]) + " " + self.get_fullname(events[i]))
                  if len(events) != 0:
                        compared = events[0]['id']

                  await asyncio.sleep(EVENT_REFRESH_DELAY)