# -*- coding: utf-8 -*-

import random
import os

class MessageDelivery():

    def __init__(self, callback, count):
        self.callback = callback
        self.count = count

        self.messageCounter = 0

    def increase(self):
        self.messageCounter += 1
        if self.messageCounter == self.count:
            self.callback()
            self.messageCounter = 0

class RandomMessages():
    
    def __init__(self):
        txt = open(os.getcwd()+"/lines.txt", encoding="utf-8")
        self.lines = txt.readlines()

    def getRandomMesssage(self):
        lineLength = len(self.lines)
        randomInt = random.randint(0, lineLength-1)
        #self.lines[randomInt].split("\"")[0]
        return self.lines[randomInt].rstrip('\n')
