import requests
import asyncio
import json
import enum
from scramjet.streams import Stream
import mailchimp_marketing
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError

requires = {
    'requires': 'pipe',
    'contentType': 'text/plain'
}

WAIT_TIME_ERROR = 3

class TopicInfo(enum.Enum):
      STRIPE = "stripe"
      AUTH0 = "auth0-user"
      A0_NEWSLETTER = "auth0-newsletter"


class ChimpInsert:
      def __init__(self, audience_id, config, slack_channel_id, slack_api_url, logger):
            self.mailchimp = Client()
            self.audience_id = audience_id
            self.mailchimp.set_config(config)
            self.slack_channel_id = slack_channel_id
            self.slack_api_url = slack_api_url
            self.token_header = {'content-type': 'application/json',}
            self.logger = logger
      
      def get_offset(self, audience_id):
            response = self.mailchimp.lists.get_list(audience_id)['stats']
            users_num = response['member_count'] + response['unsubscribe_count']
            if users_num < 5:
                  return 0
            else:
                  return users_num-5
      
      def get_info(self, info, given):
            for member in info['members']:
                  if given == member["email_address"]:
                        return member['id']
            return -1

      def prepare_member_info(self, email, fname, lname):
            member_info = {
                              "email_address": email,
                              "status":"unsubscribed",
                              "merge_fields" : {
                                    "FNAME":fname,
                                    "LNAME":lname.replace("\n", "")
                  }}
            return member_info
      
      def insert_info(self, info):

            try:
                  email, fname, lname = info.split(" ")
            except ValueError:
                  self.logger.info("ChimpInsert: Bad data received at topic")
                  return
            
            member_info = {}

            try:
                  member_info = self.prepare_member_info(email, fname, lname)
            except:
                  self.logger.info("ChimpInsrt: No data received")
                  return


            if TopicInfo.AUTH0.value in lname:
                  try:
                        response = self.mailchimp.lists.add_list_member(self.audience_id, member_info)
                        self.logger.info("ChimpInsert: Auth0 user successfully added")
                        slack_message_resp = requests.post(self.slack_api_url, headers=self.token_header, data=str({"text":f"{email} Auth0 user successfully added"}))
                  except ApiClientError as error:
                        return
                  
            
            elif TopicInfo.A0_NEWSLETTER.value in lname:
                  try:
                        member_info['status'] = "subscribed"
                        response = self.mailchimp.lists.add_list_member(self.audience_id, member_info)
                        self.logger.info(f"ChimpInsert: {email} Auth0 user with newsletter successfully added")
                        slack_message_resp = requests.post(self.slack_api_url, headers=self.token_header, data=str({"text":f"{email} Auth0 user with newsletter successfully added"}))
                  except ApiClientError as error:
                        error = json.loads(error.text)
                        if error["title"] == "Member Exists":
                              response = self.mailchimp.lists.get_list_members_info(self.audience_id, offset=self.get_offset(self.audience_id))
                              user_id = self.get_info(response, email)
                              if user_id == -1:
                                    return
                              response = self.mailchimp.update_list_member(self.audience_id, user_id, {"status" : "subscribed"})
                              self.logger.info(f"ChimpInsert: {email} Auth0 user with newsletter successfully added")

            elif TopicInfo.AUTH0.stripe in lname:
                  response = self.mailchimp.lists.get_list_members_info(self.audience_id, offset=self.get_offset(self.audience_id))
                  user_id = self.get_info(response, email)
                  if user_id == -1:
                        return
                  response = self.mailchimp.lists.update_list_member_tags(self.audience_id, user_id, {"tags" : [{"name": "Stripe", "status": "active"}]})
                  self.logger.info(f"ChimpInsert: {email} Stripe user successfully synchronized")
                  slack_message_resp = requests.post(self.slack_api_url, headers=self.token_header, data=str({"text":f"{email} Stripe user successfully synchronized"}))
            

async def run(context, input):
      try:
            slack_channel_id = context.config['slack_channel_id']
            slack_api_url = context.config['slack_api_url']
            audience_id = context.config['audience_id']
            config = {"api_key": context.config['mailchimp_api'], "server": context.config['mailchimp_server']}  
      except Exception as error:
            raise Exception(f"ChimpInsert: Config not loaded: {error}")

      inserter = ChimpInsert(audience_id, config, slack_channel_id, slack_api_url, context.logger)
      return input.each(inserter.insert_info)