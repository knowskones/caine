# -*- coding: utf-8 -*-
from linepy import *
from commands import commands

client = LINE()
#client = LINE('authToken')
client.log("Auth Token : " + str(client.authToken))
tracer = OEPoll(client)
profile = client.getProfile()
settings = client.getSettings()
if settings.e2eeEnable == True:
    raise Exception("You must disable Letter Sealing.")

setup_file = "stored_info.json"
do = commands()
do.setup(setup_file)

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    """
     - op.param1 is group id
    """
    try:
        if do.welcome_message[op.param1][1] == "on":
            client.sendMessage(to=op.param1, text=do.welcome_message[op.param1][0])
    except Exception as e:
        print(e)

def NOTIFIED_ADD_CONTACT(op):
    """
     - op.param1 is uid of contact
    """
    try:
        if (do.add_message[1] == "on") and (len(do.add_message[0]) != 0):
            client.sendMessage(to=op.param1, text=do.add_message[0])
    except Exception as e:
        print(e)

def RECEIVE_MESSAGE(op):
    try:
        msg = op.message
        msg.from_ = msg._from
        if msg.toType == 0:
            msg.to = msg.from_
        text = msg.text.rstrip()
        commands = [c[0] for c in do.custom_commands]
        responses = [r[1] for r in do.custom_commands]
        if text in commands:
            index = commands.index(text)
            response = responses[index]
            client.sendMessage(to=msg.to, text=response)
    except Exception as e:
        print(e)

def SEND_MESSAGE(op):
    try:
        msg = op.message
        msg.from_ = msg._from
        if msg.toType == 0 and (msg.from_!=profile.mid):
            msg.to = msg.from_
        text = msg.text.rstrip()
        if text.lower() == "help":
            string = "## HELP ##\n"
            for h in do.help_message:
                if h[0] == "\n":
                    h = h[1:]
                    string += "\n\n%s%s" % (do.rname,h)
                else:
                    string += "\n%s%s" % (do.rname,h)
            client.sendMessage(to=msg.to, text=string)
        elif text.lower() in ["rname","responsename"]:
            client.sendMessage(to=msg.to, text=do.rname)
        elif text[:len(do.rname)] == do.rname:
            text = text[len(do.rname):]
            if text.lower() == "help":
                string = "## HELP ##\n"
                for h in do.help_message:
                    if h[0] == "\n":
                        h = h[1:]
                        string += "\n\n%s%s" % (do.rname,h)
                    else:
                        string += "\n%s%s" % (do.rname,h)
                client.sendMessage(to=msg.to, text=string)
            elif text.lower() == "mid":
                client.sendMessage(to=msg.to, text=msg.from_)
            elif text.lower() == "gid":
                if msg.toType == 2:
                    client.sendMessage(to=msg.to, text=msg.to)
                else:
                    client.sendMessage(to=msg.to, text="This is not a group.")
            elif text.lower() == "gpic":
                if msg.toType == 2:
                    picture_url = "http://dl.profile.line.naver.jp/"
                    group = client.getGroup(msg.to)
                    picture_url += group.pictureStatus
                    client.sendImageWithURL(to=msg.to, url=picture_url)
                else:
                    client.sendMessage(to=msg.to, text="This is not a group.")
            elif text.lower() in ["rname","responsename"]:
                client.sendMessage(to=msg.to, text=do.rname)
            elif text.lower() == "welcome message":
                if msg.toType == 2:
                    if msg.to in do.welcome_message.keys():
                        wm = do.welcome_message[msg.to][0]
                        toggle = do.welcome_message[msg.to][1]
                        client.sendMessage(to=msg.to, text="Your welcome message (currently set to %s):\n%s" % (wm,toggle))
                    else:
                        client.sendMessage(to=msg.to, text="You have not set a welcome message for this group.")
                else:
                    client.sendMessage(to=msg.to, text="This is not a group; it has no welcome message.")
            elif text.lower() == "add message":
                am = do.add_message[0]
                toggle = do.add_message[1]
                if len(am) == 0:
                    client.sendMessage(to=msg.to, text="You do not have an add message set.")
                else:
                    client.sendMessage(to=msg.to, text="Your add message (currently set to %s):\n%s" % (am,toggle))
            elif text[:12].lower() == "update rname":
                if len(text) == 12:
                    client.sendMessage(to=msg.to, text="Rname cannot be blank.")
                else:
                    do.updateRname(text[13:])
                    client.sendMessage(to=msg.to, text="Rname updated:\n%s" % do.rname)
            elif text[:19].lower() == "set welcome message":
                if msg.toType == 2:
                    if len(text) <= 20:
                        client.sendMessage(to=msg.to, text="Message cannot be blank.")
                    else:
                        do.updateWM(msg.to,text[20:])
                        client.sendMessage(to=msg.to, text="Welcome message updated:\n%s" % do.welcome_message[msg.to][0])
                else:
                    client.sendMessage(to=msg.to, text="This is not a group; you cannot set a welcome messag here.")
            elif text[:15].lower() == "set add message":
                if len(text) == 15:
                    client.sendMessage(to=msg.to, text="Message cannot be blank.")
                else:
                    do.updateAM(text[16:])
                    client.sendMessage(to=msg.to, text="Add message updated:\n%s" % do.add_message[0])
            elif text.lower() == "remove welcome message":
                if msg.to in do.welcome_message.keys():
                    do.removeWM(msg.to)
                    client.sendMessage(to=msg.to, text="Welcome message removed.")
                else:
                    client.sendMessage(to=msg.to, text="You have not set a welcome message for this group.")
            elif text.lower() == "remove add message":
                do.removeAM()
                client.sendMessage(to=msg.to, text="Add message removed.")
            elif text.lower() == "remove all welcome messages":
                do.clearWM()
                client.sendMessage(to=msg.to, text="Welcome messages cleared.")
            elif text.lower() == "add message:on":
                do.toggleAM("on")
                client.sendMessage(to=msg.to, text="Add message has been turned on.")
            elif text.lower() == "add message:off":
                do.toggleAM("off")
                client.sendMessage(to=msg.to, text="Add message has been turned off.")
            elif text.lower() == "welcome message:on":
                if msg.to in do.welcome_message.keys():
                    do.toggleWM(msg.to,"on")
                    client.sendMessage(to=msg.to, text="Welcome message has been turned on.")
                else:
                    client.sendMessage(to=msg.to, text="This group does not have a welcome message set.")
            elif text.lower() == "welcome message:off":
                if msg.to in do.welcome_message.keys():
                    do.toggleWM(msg.to,"off")
                    client.sendMessage(to=msg.to, text="Welcome message has been turned off.")
                else:
                    client.sendMessage(to=msg.to, text="This group does not have a welcome message set.")
            elif text[:18].lower() == "set custom command":
                text_list = text[19:].split()
                command = text_list[0].rstrip()
                current_commands = [pair[0] for pair in do.custom_commands]
                if command in current_commands:
                    client.sendMessage(to=msg.to, text="You already have a response set for this command.")
                else:
                    response = text[20+len(command):].rstrip()
                    do.addCC(command,response)
                    client.sendMessage(to=msg.to, text="Custom command %s added." % command)
            elif text.lower() == "show custom commands":
                string = "##Custom Commands##\n"
                string += "(%s commands)\n" % len(do.custom_commands)
                for i in range(len(do.custom_commands)):
                    string += "\n%s." % i
                    string += "\n[%s]" % do.custom_commands[i][0]
                    string += "\n[%s]" % do.custom_commands[i][1]
                client.sendMessage(to=msg.to, text=string)
            elif text[:21].lower() == "remove custom command":
                numbertext = text[21:]
                numbers = do.numberTextToList(numbertext)
                allowed_numbers = [n for n in numbers if n < len(do.custom_commands)]
                if len(allowed_numbers) == 0:
                    client.sendMessage(to=msg.to, text="You did not include any valid numbers.")
                else:
                    commands_removed = []
                    for an in allowed_numbers:
                        commands_removed.append(do.custom_commands[an][0])
                        do.removeCC(an)
                    string = "Commands removed (%s):\n" % len(commands_removed)
                    for cr in commands_removed:
                        string += "\n[%s]" % cr
                    client.sendMessage(to=msg.to, text=string)
            elif text.lower() == "remove all custom commands":
                do.clearCC()
                client.sendMessage(to=msg.to, text="All custom commands removed.")
            commands = [c[0] for c in do.custom_commands]
            responses = [r[1] for r in do.custom_commands]
            if text in commands:
                index = commands.index(text)
                response = responses[index]
                client.sendMessage(to=msg.to, text=response)
    except Exception as e:
        print(e)

tracer.addOpInterruptWithDict({
    OpType.SEND_MESSAGE: SEND_MESSAGE,
    OpType.NOTIFIED_ADD_CONTACT: NOTIFIED_ADD_CONTACT,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.RECEIVE_MESSAGE: RECEIVE_MESSAGE
})

while True:
    tracer.trace()
