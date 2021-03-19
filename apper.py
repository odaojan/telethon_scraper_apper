import configparser, json, time, traceback, random

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerChannel, InputPeerUser
from telethon.sync import TelegramClient
from telethon import functions, types

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

	json_file = input('Enter path to json file with users: ').strip()
	channel_name = input('Enter the name of the channel where to invite users: ').strip()
	
	channel = client.get_entity(channel_name)
	target_channel_entity = InputPeerChannel(channel.id, channel.access_hash)

	with open(json_file, 'r') as json_fp:
		users = json.load(json_fp)
		for user in users:
			try:
				print("Adding {}".format(user['id']))

				user_to_add = InputPeerUser(user['id'], user['access_hash'])
				result = client(InviteToChannelRequest(target_channel_entity, [user_to_add]))
				print(result.stringify())

				print("Waiting for 60-90 Seconds...")
				time.sleep(random.randrange(5, 6))
			except PeerFloodError:
				print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
				print("Waiting {} seconds".format(100))
				time.sleep(100)
			except UserPrivacyRestrictedError:
				print("The user's privacy settings do not allow you to do this. Skipping.")
				print("Waiting for 2 Seconds...")
				time.sleep(2)
			except:
				traceback.print_exc()
				print("Unexpected Error")
				continue
	