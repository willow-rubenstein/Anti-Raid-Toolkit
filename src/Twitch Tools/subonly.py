import requests
import time
from threading import Thread
import json
from websocket import create_connection

class oauthToken:
  def __init__(self):
      self.credentials = json.load(open('credentials.json'))
    
  def getToken(self):
      r = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={self.credentials['id']}&client_secret={self.credentials['secret']}&grant_type=client_credentials")
      return f"Bearer {r.json()['access_token']}"

with open('users.json', 'r') as f:
  users = json.load(f)['users']

credentials = json.load(open('credentials.json'))
cid = credentials['id']
secret = credentials['secret']
o = oauthToken()
api = o.getToken()
irc = credentials['irc']

def emotesOnly(status, username):
    ws = create_connection('wss://irc-ws.chat.twitch.tv')
    ws.send(f'PASS {irc}')
    ws.send(f'NICK hateraidsbgone')
    ws.send(f'JOIN #{username}')
    if status == 1:
        print(f'turning subscribers-only on for user {username}')
        ws.send(f"PRIVMSG #{username} :/subscribers")
    else:
        print(f'turning subscribers-only off for user {username}')
        ws.send(f"PRIVMSG #{username} :/subscribersoff")
    ws.close()

def channelLive(username):
    global api
    global cid
    headers = {'Accept': 'application/vnd.twitchtv.v5+json', "Client-Id": cid, "Authorization": api}
    r = requests.get(f'https://api.twitch.tv/helix/streams?user_login={username}', headers=headers).json()
    if r['data'] == []:
        return False
    else:
        return True

loopJson = {}
def mainLoopThread(item):
  global loopJson
  if channelLive(item) == False and loopJson[item] != True:
    loopJson[item] = True
    emotesOnly(1, item)
  elif channelLive(item) == True and loopJson[item] != False:
    loopJson[item] = False
    emotesOnly(0, item)

def mainLoop(users=[]):
    global loopJson
    for item in users:
        loopJson[item] = None
    while True:
        for item in users:
            th = Thread(target=mainLoopThread, args=(item,))
            th.start()
        time.sleep(2.5)

Thread(target=mainLoop, args=(users,)).start() 
