# -*- coding: utf-8 -*-

from time import time

from . import commands
from . import messages

PREFIX = "!"


class Cmd(object):
	def __init__(self, callables, func, cooldown=0):
		self.callables = callables
		self.func = func
		self.cooldown = cooldown
		self.next_use = time()


# cmds = {
# 	"hello": commands.hello,
# }

cmds = [
	#	commands
	Cmd(["hello", "hi", "hey"], commands.hello, cooldown=15),
	#Cmd(["userinfo", "ui"], commands.userinfo),
	Cmd(["discord", "dc"], commands.discord, cooldown=15),
	Cmd(["streamplan"], commands.streamplan, cooldown=15),
	Cmd(["twitchprime", "prime"], commands.twitchprime, cooldown=15),
	Cmd(["spenden", "donation", "tip"], commands.spenden, cooldown=15),
	Cmd(["streamingprojekt", "streamprojekt", "projekt"], commands.projekt, cooldown=15),
	Cmd(["change", "set", "changecmd"], commands.changeCmd, cooldown=15),
	Cmd(["feedback", "vorschlag", "verbesserung"], commands.feedback, cooldown=15),
	Cmd(["streampartner", "streamingpartner", "multi"], commands.streampartner, cooldown=15)
]


def process(bot, user, message):

	if message.startswith(PREFIX):
		cmd = message.split(" ")[0][len(PREFIX):]
		args = message.split(" ")[1:]
		perform(bot, user, cmd, *args)


def perform(bot, user, call, *args):
	if call in ("help", "commands", "cmds"):
		commands.help(bot, PREFIX, cmds)

	else:
		for cmd in cmds:
			if call in cmd.callables:
				if time() > cmd.next_use:
					cmd.func(bot, user, *args)
					cmd.next_use = time() + cmd.cooldown

				else:
					bot.send_message(f"Cooldown still in effect. Try again in {cmd.next_use-time():,.0f} seconds.")

				return

		#bot.send_message(f"{user['name']}, \"{call}\" isn't a registered command.")
