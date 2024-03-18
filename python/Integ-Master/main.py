
from auth0_reader import Auth0
from stripe_reader import Stripe
import json
import asyncio
from scramjet.streams import Stream



provides = {
    'provides': 'pipe',
    'contentType': 'text/plain'
}

class Master:
      def __init__(self, auth0_client, stripe_client, stream) -> None:
            self.auth0_client = auth0_client
            self.stripe_client = stripe_client
            self.stream = stream
      

      async def read(self):
            stripe_task = asyncio.create_task(self.stripe_client.get_event())
            auth0_task = asyncio.create_task(self.auth0_client.get_auth())
            
            await asyncio.gather(stripe_task, auth0_task, return_exceptions=True)
            

async def run(context, input):
      config = context.config
      stream = Stream()

      try:
            run.verified_url = config["auth0_verified_url"]
            run.users_url = config["auth0_users_url"] 
            run.api_url = config["api_url"]
            run.data = json.dumps(config["request_data"])
            run.stripe_api= config["stripe_api"]
      except Exception as error:
            raise Exception(f"Master: Config not loaded: {error}")

      auth0_client = Auth0(run.verified_url, run.users_url , run.api_url, run.data, stream, context.logger)
      stripe_client = Stripe (run.stripe_api, stream, context.logger)

      asyncio.gather(
                  Master(auth0_client, stripe_client, stream).read(),
                  return_exceptions=True,
            )
      return stream.map(lambda x: x + "\n")
