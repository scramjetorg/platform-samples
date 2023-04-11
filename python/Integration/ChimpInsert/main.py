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
    result = info["members"]
    for i in range(0, len(result)):
        if given == result[i]["email_address"]:
            return result[i]["id"]
            
async def insert_info(info):
	response = mailchimp.ping.get()
	info = info.split(" ")
	try:
		print(info[0],info[1] , info[2])
		member_info = {
				"email_address": info[0],
				"status":"unsubscribed",
				"merge_fields" : {
					"FNAME":info[1],
					"LNAME":info[2].replace("\n", "")
		}}
		try:
			response = mailchimp.lists.add_list_member(run.audience_id, member_info)
			#print(response);
		except ApiClientError as error:
			print("An exception occurred: {}".format(error.text))
			error = json.loads(error.text)
			if error["title"] == "Member Exists":
				try:
					response = mailchimp.lists.get_list_members_info(run.audience_id)
					user_id = get_info(response, info[0])
					response = mailchimp.lists.update_list_member(run.audience_id, user_id, {"status" : "subscribed"})			
				except ApiClientError as err:
					info =""	

	except:
		info = "Brak danych"
		print(info);

async def run(context, input):
	run.audience_id = context.config['audience_id']
	mailchimp.set_config({
	  "api_key": context.config['mailchimp_api'],
	  "server": context.config['mailchimp_server'],
	})
	stream = Stream()
	return input.each(insert_info)
	
	
	
