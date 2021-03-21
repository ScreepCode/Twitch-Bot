# -*- coding: utf-8 -*-

from irc.bot import SingleServerIRCBot
from requests import get

from lib import cmds
from lib.cmds.messages import MessageDelivery
from lib.cmds.messages import RandomMessages

import os


NAME = "screepcodebot"
OWNER = "screepcode"
FIRE_MESSAGE_TRESHOLD = 20

class Bot(SingleServerIRCBot):
	def __init__(self):
		
		file = open(os.getcwd()+"/Secret/login.txt","r")
		login = file.readlines()
		file.close()
		
		self.HOST = "irc.chat.twitch.tv"
		self.PORT = 6667
		self.USERNAME = NAME.lower()
		self.CLIENT_ID = login[0].split(":")[0]
		self.TOKEN = login[1].split(":")[0]
		self.CHANNEL = f"#{OWNER}"

		url = f"https://api.twitch.tv/kraken/users?login={OWNER}"
		headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
		resp = get(url, headers=headers).json()
		self.channel_id = resp["users"][0]["_id"]

		super().__init__([(self.HOST, self.PORT, f"oauth:{self.TOKEN}")], self.USERNAME, self.USERNAME)

		#Variabeln
		self.messageCounter = 0


		self.randomMessages = RandomMessages()
		self.messageDelivery = MessageDelivery(self.randomMessageSend, FIRE_MESSAGE_TRESHOLD)
		


	def on_welcome(self, cxn, event):
		for req in ("membership", "tags", "commands"):
			cxn.cap("REQ", f":twitch.tv/{req}")

		cxn.join(self.CHANNEL)
		#self.send_message("Now online.")
		print("Now online")

	def on_pubmsg(self, cxn, event):
		tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
		user = {"name": tags["display-name"], "id": tags["user-id"]}
		message = event.arguments[0]

		if user["name"] != NAME:
			cmds.process(bot, user, message.lower())

		self.messageDelivery.increase()


	def send_message(self, message):
		self.connection.privmsg(self.CHANNEL, message)

	def randomMessageSend(self):
		self.send_message(self.randomMessages.getRandomMesssage())

if __name__ == "__main__":
	bot = Bot()
	bot.start()
