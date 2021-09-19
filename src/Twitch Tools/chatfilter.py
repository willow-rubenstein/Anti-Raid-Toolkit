"""
   Copyright 2021 Ashe Muller

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from websocket import create_connection
from twitchio.ext import commands
from threading import Thread
import re
import json

emojis = [char for char in open('emojis.txt', encoding="utf-8").read()]

def is_emoji(s):
  if s not in emojis:
    return False
  else:
    return True

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
