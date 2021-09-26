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
from threading import Thread
import json

botNames = ['hoss', 'gunz0', 'zachsapttv', 'zachsaptv', 'blueberrydogs', 'ho03012ss']
credentials = json.load(open('credentials.json'))
irc = credentials['twitch']['irc']


def addToBanlist(username):
    followlist = json.load(open('banlist.json'))['users']
    if username not in followlist:
        followlist.append(username)
    json.dump({"users": followlist}, open('banlist.json', 'w+'), indent=4)
    
def banUser(username, broadcaster_name):
    print(f"Malicious follower event recieved for {broadcaster_name} (username: {username}). Banning from channel.")
    addToBanlist(username)
    ws = create_connection('wss://irc-ws.chat.twitch.tv')
    ws.send(f"PASS {irc}")
    ws.send(f'NICK hateraidsbgone')
    ws.send(f"PRIVMSG #{broadcaster_name} :/ban {username}")
    ws.close()

def logic(feed):
    eventData = feed['event']
    print(f"Beginning logic check on user {eventData['user_login']} in channel {eventData['broadcaster_user_login']}")
    failedChecks = 0
    for item in botNames:
        if eventData['user_login'].find(item) != -1:
            failedChecks += 1
    if failedChecks > 0:
        Thread(target=banUser, args=(eventData['user_login'], eventData['broadcaster_user_login'],)).start()
    else:
        print(f"Account {eventData['user_login']} failed no checks.")
