import configparser
import json

from telethon.sync import TelegramClient
from telethon import errors

from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch

print("""
 __    __     ______     __     __     ______     __   __    
/\ "-./  \   /\  == \   /\ \  _ \ \   /\  __ \   /\ "-.\ \   
\ \ \-./\ \  \ \  __<   \ \ \/ ".\ \  \ \  __ \  \ \ \-.  \  
 \ \_\ \ \_\  \ \_\ \_\  \ \__/".~\_\  \ \_\ \_\  \ \_\\"\_\ 
  \/_/  \/_/   \/_/ /_/   \/_/   \/_/   \/_/\/_/   \/_/ \/_/ 
                                                             
""")

config = configparser.ConfigParser()
config.read("config.ini")

api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

with TelegramClient(username, api_id, api_hash) as client:

	url = input('Еnter the link to the channel or chat:').strip()
	json_filename = url.split('/')[-1].strip()
	channel = client.get_entity(url)

	offset_user = 0    # the participant number from which the reading starts 
	limit_user = 100   # maximum number of records transferred at one time 

	all_participants = []   # list of all channel members 
	filter_user = ChannelParticipantsSearch('')

	while True:
		try:
			participants = client(GetParticipantsRequest(channel,
				filter_user, offset_user, limit_user, hash=0))
		except errors.ChatAdminRequiredError as privilegesError:
			print(privilegesError)
			break	
		if not participants.users:
			break
		all_participants.extend(participants.users)
		offset_user += len(participants.users)

	all_users_details = []   # list of dictionaries with interesting parameters of channel members 

	for participant in all_participants:
			all_users_details.append({"id": participant.id,
				"first_name": participant.first_name,
				"last_name": participant.last_name,
				"user": participant.username,
				"phone": participant.phone,
				"access_hash": participant.access_hash,
				"is_bot": participant.bot})

	with open('data/' + json_filename + '.json', 'w', encoding='utf8') as outfile:
		json.dump(all_users_details, outfile, ensure_ascii=False, indent=4)
