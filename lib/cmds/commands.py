# -*- coding: utf-8 -*-

from datetime import timedelta
from sys import exit
from time import time
import sqlite3
import os

OWNER = "screepcode"

ModeratorRechte = ["87172988"]


def help(bot, prefix, cmds):
	#bot.send_message(f"Registered commands: "
	#	+ ", ".join([f"{prefix}{cmd.callables[0]}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))

	bot.send_message(f"Registered commands (incl. aliases): "
		+ ", ".join([f"{prefix}{'/'.join(cmd.callables)}" for cmd in sorted(cmds, key=lambda cmd: cmd.callables[0])]))


def hello(bot, user, *args):
	bot.send_message(f"Hey {user['name']} ^^")

def userinfo(bot, user, *args):
	bot.send_message(f"Name: {user['name']}. ID: {user['id']}.")

def discord(bot, user, *args):
	bot.send_message(SQLRead("discord"))

def streamplan(bot, user, *args):
	bot.send_message(SQLRead("streamplan"))

def twitchprime(bot, user, *args):
	bot.send_message(SQLRead("twitchprime"))
	
def spenden(bot, user, *args):
	bot.send_message(SQLRead("spenden"))

def projekt(bot, user, *args):
	bot.send_message(SQLRead("projekt"))

def streampartner(bot, user, *args):
	bot.send_message(SQLRead("streampartner"))

def feedback(bot, user, *args):
	if len(args) > 0:
		try:
			feedback = " ".join(args)
			with open(os.getcwd()+"/Feedback.txt", "a", encoding="utf-8") as txt:
				txt.writelines(feedback + "\n")
			bot.send_message("Vielen Dank für dein Feedback ^^")

		except:
			bot.send_message("Ein Fehler ist bei der Feedbackübermittlung aufgetreten :/")
	else:
		bot.send_message("Gebe bitte noch deine Nachricht an ^^")
	



def changeCmd(bot, user, *args):
	hasPermission = False
	
	for Mod in ModeratorRechte:
		if Mod == user["id"]:
			hasPermission = True

	if hasPermission == True:
		try:
			#print("Funktion: " + args[0] + " Neuer Inhalt: " + args[1])
			SQLWrite(args[0], " ".join(args))
		except:
			bot.send_message("Ein Fehler bei der Funktion ist aufgetreten")
	else:
		bot.send_message("Du hast keine Rechte um diesen Befehl auszuführen")


def SQLWrite(Funktion, Inhalt):
	Inhalt = Inhalt[(len(Funktion) + 1):]
	connection = sqlite3.connect("cmds.db")
	cursor = connection.cursor()
	cursor.execute("""UPDATE main.cmds SET Inhalt = ? WHERE Funktion = ?;""", (Inhalt, Funktion))
	#cursor.execute("UPDATE main.cmds SET Inhalt = '" + Inhalt + "' WHERE Funktion = '" + Funktion + "'")
	connection.commit()
	cursor.close()
	connection.close()

def SQLRead(Funktion):
	connection = sqlite3.connect("cmds.db")
	cursor = connection.cursor()
	cursor.execute("SELECT Inhalt FROM main.cmds WHERE Funktion = '" + Funktion + "'")
	#cursor.execute("UPDATE main.cmds SET Inhalt = '" + Inhalt + "' WHERE Funktion = '" + Funktion + "'")
	Inhalt = cursor.fetchall()[0][0]
	connection.commit()
	cursor.close()
	connection.close()
	return Inhalt




def shutdown(bot, user, *args):
	if user["name"].lower() == OWNER:
		bot.send_message("Shutting down.")
		bot.disconnect()
		exit(0)

	else:
		bot.send_message("You can't do that.")
