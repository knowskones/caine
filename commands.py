# -*- coding: utf-8 -*-
import json

class commands:
    def __init__(self):
        self.rname = "."
        self.welcome_message = {} #gid:[message,on/off]
        self.add_message = ["","off"]
        self.custom_commands = []
        self.data = None
        self.json_path = None
        self.help_message = ["help",
                            "mid",
                            "gid",
                            "gpic",
                            "\nrname",
                            "welcome message",
                            "add message",
                            "show custom commands",
                            "\nupdate rname <name>",
                            "set welcome message <msg>",
                            "set add message <msg>",
                            "set custom command <cmd> <response>",
                            "\nadd message:on",
                            "add message:off",
                            "welcome message:on",
                            "welcome message:off",
                            "\nremove welcome message",
                            "remove all welcome messages",
                            "remove add message",
                            "remove custom command <nums>",
                            "remove all custom commands"]

    def setup(self, file_path):
        self.json_path = file_path
        self.data = json.load(open(file_path, "r"))
        self.rname = self.data["rname"]
        self.add_message = self.data["add_message"]
        self.welcome_message = self.data["welcome_message"]
        self.custom_commands = self.data["custom_commands"]
        print("Done.")

    def updateJson(self):
        with open(self.json_path, "w") as json_file:
            json.dump(self.data, json_file)
        print ("Done.")

    def updateRname(self,name):
        self.rname = name
        self.data["rname"] = name
        self.updateJson()

    def updateWM(self,gid,text):
        if gid in self.welcome_message.keys():
            IO = self.welcome_message[gid][1]
        else:
            IO = "off"
        self.welcome_message[gid] = [text,IO]
        self.data["welcome_message"][gid] = [text,IO]
        self.updateJson()

    def updateAM(self,text):
        self.add_message[0] = text
        self.data["add_message"][0] = text
        self.updateJson()

    def clearWM(self):
        self.welcome_message = {}
        self.data["welcome_message"] = {}
        self.updateJson()

    def removeWM(self,gid):
        del self.welcome_message[gid]
        self.updateJson()

    def removeAM(self):
        self.add_message = ["","off"]
        self.data["add_message"] = ["","off"]
        self.updateJson()

    def toggleAM(self,toggle):
        if toggle in ["on","off"]:
            self.add_message[1] = toggle
            self.data["add_message"][1] = toggle
            self.updateJson()
        else:
            raise ValueError

    def toggleWM(self,gid,toggle):
        if toggle in ["on","off"]:
            self.welcome_message[gid][1] = toggle
            self.data["welcome_message"][gid][1] = toggle
            self.updateJson()
        else:
            raise ValueError

    def addCC(self,command,response):
        self.custom_commands.append([command,response])
        self.updateJson()

    def removeCC(self,index):
        del self.custom_commands[index]
        self.updateJson()

    def clearCC(self):
        self.custom_commands = []
        self.data["custom_commands"] = []
        self.updateJson()

    def numberTextToList(self,text):
        numbertext = ""
        i = 0
        while i < len(text):
            try:
                numbertext += str(int(text[i]))
            except ValueError:
                numbertext += " "
            i += 1
        nlist = numbertext.split()
        numbers = [int(n) for n in nlist]
        set_num = set(numbers)
        numbers = list(set_num)
        numbers.sort()
        return numbers
