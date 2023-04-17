import requests
import stripe
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

def get_info(info, given):
    for member in info['members']:
    	if given == member["email_address"]:
    		return member['id']
            
async def insert_info(info):
	email, fname, lname = info.split(" ")
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
		except ApiClientError as error:
			print("An exception occurred: {}".format(error.text))
			error = json.loads(error.text)
			if error["title"] == "Member Exists":
				try:
					response = mailchimp.lists.get_list_members_info(run.audience_id)
					user_id = get_info(response, email)
					response = mailchimp.lists.update_list_member(run.audience_id, user_id, {"status" : "subscribed"})			
				except ApiClientError as err:
					print(err)	

	except:
		print("No data received.");

async def run(context, input):
	run.audience_id = context.config['audience_id']
	mailchimp.set_config({
	  "api_key": context.config['mailchimp_api'],
	  "server": context.config['mailchimp_server'],
	})
	stream = Stream()
	return input.each(insert_info)
	
	
	
