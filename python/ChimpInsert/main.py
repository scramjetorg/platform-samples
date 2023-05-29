import requests
import asyncio
import json
from scramjet.streams import Stream
import mailchimp_marketing
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError


requires = {
    'requires': 'pipe',
    'contentType': 'text/plain'
}

mailchimp = Client()

def get_offset(audience_id):
      response = mailchimp.lists.get_list(audience_id)['stats']
      users_num = response['member_count'] + response['unsubscribe_count']
      if users_num < 5:
            return 0
      else:
            return users_num-5

def get_info(info, given):
	for member in info['members']:
		if given == member["email_address"]:
			return member['id']
            
async def insert_info(info):
	try:
		email, fname, lname = info.split(" ")
	except:
		print("No data received. start")
	response = mailchimp.ping.get()
	try:
		member_info = {
				"email_address": email,
				"status":"unsubscribed",
				"merge_fields" : {
					"FNAME":fname,
					"LNAME":lname.replace("\n", "")
		}}
		try:
			response = mailchimp.lists.add_list_member(run.audience_id, member_info)
			print(f"{email} Auth0 user successfully added")
		except ApiClientError as error:
			error = json.loads(error.text)
			if error["title"] == "Member Exists":
				try:
					response = mailchimp.lists.get_list_members_info(run.audience_id, offset=get_offset(run.audience_id))
					user_id = get_info(response, email)
					response = mailchimp.lists.update_list_member(run.audience_id, user_id, {"status" : "subscribed"})
					print(f"{email} Stripe user successfully synchronized")	
				except ApiClientError as err:
					print("Error")	
	except:
		print("No data received.")

async def run(context, input):
	run.audience_id = context.config['audience_id']
	mailchimp.set_config({
	  "api_key": context.config['mailchimp_api'],
	  "server": context.config['mailchimp_server'],
	})
	return input.each(insert_info)
	
	
	
