import requests
import asyncio
import json
import enum
import hashlib
from scramjet.streams import Stream
import mailchimp_marketing
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

requires = {
    'requires': 'pipe',
    'contentType': 'text/plain'
}

WAIT_TIME_ERROR = 3
REQUEST_DELAY = 1
TASK_DELAY = 0.5


class TopicInfo(enum.Enum):
      STRIPE = "stripe"
      AUTH0 = "auth0-user"
      A0_NEWSLETTER = "auth0-newsletter"

class SlackHookResponse(enum.Enum):
      SUCCESS = 200
      FAILURE = 0
      NOT_SENT = -1

class InsertionResponse(enum.Enum):
      SUCCESS = 200
      API_ERROR = 400
      FAILURE = 0



class ChimpInsert:
      def __init__(self, audience_id, config, slack_api_url, logger):
            self.mailchimp = Client()
            self.audience_id = audience_id
            self.mailchimp.set_config(config)
            self.slack_api_url = slack_api_url
            self.token_header = {'content-type': 'application/json',}
            self.logger = logger

      async def post_slackMSG(self, text):
            try:
                  response = requests.post(self.slack_api_url, headers=self.token_header, data=str({"text":f"{text}"}))
            except Exception as error:
                return SlackHookResponse.FAILURE.value
            
            if response.status_code != SlackHookResponse.SUCCESS.value:
                  return SlackHookResponse.FAILURE.value
            
            return SlackHookResponse.SUCCESS.value
      
      async def handle_auth0_user(self, email, member_info):
            try:
                  self.mailchimp.lists.add_list_member(self.audience_id, member_info)

                  self.logger.info(f"ChimpInsert: {email} - Auth0 user successfully added.")
                  return InsertionResponse.SUCCESS.value
            
            except ApiClientError:
                  return InsertionResponse.API_ERROR.value
            except Exception:
                  return InsertionResponse.FAILURE.value
            
      async def handle_auth0_newsletter_user(self, email, member_info):
            try:
                  member_info['status'] = "subscribed"
                  self.mailchimp.lists.add_list_member(self.audience_id, member_info)

                  self.logger.info(f"ChimpInsert: {email} Auth0 user with newsletter successfully added.")

                  return InsertionResponse.SUCCESS.value
            
            except ApiClientError as error:
                  error = json.loads(error.text)
                  if error["title"] == "Member Exists":
                        user_id = self.get_info(email)
                        await asyncio.sleep(REQUEST_DELAY)

                        try:
                              self.mailchimp.lists.update_list_member(self.audience_id, user_id, {"status" : "subscribed"})
                              self.logger.info(f"ChimpInsert: {email} Auth0 user updated.")
                              return InsertionResponse.SUCCESS
                        
                        except ApiClientError as update_error:
                              self.logger.error(f"ChimpInsert: Error updating Auth0 user: {update_error}")
                              return InsertionResponse.API_ERROR
                        
                  self.logger.error(f"ChimpInsert: Error adding Auth0 user with newsletter: {error}")
                  return InsertionResponse.FAILURE.value
            
            

      async def handle_stripe_user(self, email):
            try:
                  user_id = self.get_info(email)
                  
                  self.mailchimp.lists.update_list_member_tags(self.audience_id, user_id, {"tags" : [{"name": "Stripe", "status": "active"}]})

                  self.logger.info(f"ChimpInsert: {email} Stripe user successfully synchronized")
                  return InsertionResponse.SUCCESS.value
            
            except ApiClientError as api_error:
                  self.logger.error(f"ChimpInsert: Mailchimp API error: {api_error}")
                  return InsertionResponse.FAILURE.value
            
            except Exception as e:
                  self.logger.error(f"ChimpInsert: Unexpected error: {e}")
                  return InsertionResponse.FAILURE.value
            

      def get_info(self, email):
            bytes_of_message = email.lower().encode('utf-8')
            md = hashlib.md5()
            md5 = md.update(bytes_of_message)
            email_hash = md.hexdigest()
            return email_hash

      def prepare_member_info(self, email, fname, lname):
            member_info = {
                              "email_address": email,
                              "status":"unsubscribed",
                              "merge_fields" : {
                                    "FNAME":fname,
                                    "LNAME":lname.replace("\n", "")
                  }}
            return member_info
      
      async def insert_info(self, info):
            try:
                  email, fname, lname = info.split(" ")
            except ValueError:
                  self.logger.info("ChimpInsert: Bad data received at topic")
                  return

            member_info = {}

            try:
                  member_info = self.prepare_member_info(email, fname, lname)
            except:
                  self.logger.info("ChimpInsert: No data received")
                  return

            slack_message_resp = SlackHookResponse.NOT_SENT.value
            status = InsertionResponse.FAILURE.value


            if TopicInfo.AUTH0.value in lname:
                  status = await self.handle_auth0_user(email, member_info)

                  if status == InsertionResponse.SUCCESS.value:
                        await asyncio.sleep(REQUEST_DELAY)
                        await self.post_slackMSG(f"{email} - Auth0 user successfully added.")

            elif TopicInfo.A0_NEWSLETTER.value in lname:
                  status = await self.handle_auth0_newsletter_user(email, member_info)

                  if status == InsertionResponse.SUCCESS.value:
                        await asyncio.sleep(REQUEST_DELAY)
                        slack_message_resp = await self.post_slackMSG(f"{email} - Auth0 user with newsletter successfully added.")

            elif TopicInfo.STRIPE.value in lname:
                  status = await self.handle_stripe_user(email)

                  if status == InsertionResponse.SUCCESS.value:
                        await asyncio.sleep(REQUEST_DELAY)
                        slack_message_resp = await self.post_slackMSG(f"{email} - Stripe user successfully added.")
                  

            
            if status == InsertionResponse.FAILURE.value:
                  self.logger.error(f"ChimpInsert: Insertion failed.")

            if slack_message_resp == SlackHookResponse.FAILURE.value:
                  self.logger.error("Slack: Failed to send message.")

            elif slack_message_resp == SlackHookResponse.NOT_SENT.value:
                  self.logger.error(f"Slack: Duplicated request - ({email})")

            else:
                  self.logger.info("Slack: Message sent successfully.")
            

async def run(context, input):
      try:  
            slack_api_url = context.config['slack_hook_url']
            audience_id = context.config['audience_id']
            config = {"api_key": context.config['mailchimp_api'], "server": context.config['mailchimp_server']}  
      except Exception as error:
            raise Exception(f"ChimpInsert: Config not loaded: {error}")

      inserter = ChimpInsert(audience_id, config, slack_api_url, context.logger)
      
      async for item in input:
            await inserter.insert_info(item)


