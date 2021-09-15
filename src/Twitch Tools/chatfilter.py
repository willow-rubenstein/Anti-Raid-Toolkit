from websocket import create_connection
from twitchio.ext import commands
from threading import Thread
import re
from emoji import UNICODE_EMOJI
import json

def is_emoji(s):
    return s in UNICODE_EMOJI['en']

users = []
print(f"Starting chatFilter processes")
credentials = json.load(open('credentials.json'))
irc = credentials['irc']

def evaluation(message, msgSender, username):
    with open('unicode.txt', 'r', encoding="utf8") as f:
        unicode = list(f.readline())
    failed = 0
    pattern = f"user-type= :{msgSender.lower()}!{msgSender.lower()}@{msgSender.lower()}.tmi.twitch.tv privmsg #{username.lower()} :"
    send = re.sub(pattern, '', message.lower())
    try:
      send.strip('"')
    except:
      pass
    try:
      send.strip("'")
    except:
      pass
    for character in send:
        if character not in unicode and is_emoji(character) == False:
          failed += 1
    if failed > 0:
        print(f"Potentially malicious message found in channel {username}. Full message: {send}.")
        return False
    else:
        return True

def deleteMessage(messageID, username):
    ws = create_connection('wss://irc-ws.chat.twitch.tv')
    ws.send(f"PASS {irc}")
    ws.send(f'NICK hateraidsbgone')
    ws.send(f"PRIVMSG #{username} :/delete {messageID}")
    ws.close()

def chatLogic(messageIn, msgID, msgSender, username):
    if evaluation(messageIn, msgSender, username) == False:
        deleteMessage(msgID, username)

bot = commands.Bot(token=irc, prefix='@', initial_channels=users)

@bot.event()
async def event_ready():
    print("Bot started successfully.")
    
@bot.event()
async def event_message(message):
    username = message.channel.name
    print(f"message event recieved for channel {username}")
    try:
        msg = message.raw_data.split(';')
        for item in msg:
          if str(item).find('user-type') != -1:
            msgObject = str(item)
        msgSender = message.tags['display-name']
        msgID = message.tags['id']
        pattern = f'user-type= :{msgSender}!{msgSender}@{msgSender}.tmi.twitch.tv PRIVMSG #{username} :'
        send = re.sub(pattern, '', msgObject).lower()
        th = Thread(target=chatLogic, args=(send,msgID,msgSender,username))
        th.start()
    except Exception as E:
      print(f"An exception has occured. Full traceback: {E}")  
bot.run()
