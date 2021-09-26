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

import requests
import json
from os import path

file_path = path.abspath(__file__)
dir_path = path.dirname(file_path)
credentials_path = path.join(dir_path,'credentials.json')

class registerEventsub:
    def __init__(self, name=None):
        self.name = name
        self.credentials = json.load(open(credentials_path))
        self.accessToken = self.getToken()
        if name != None:
            self.userId = self.getIdFromName()
    
    def getToken(self):
        r = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={self.credentials['twitch']['id']}&client_secret={self.credentials['twitch']['secret']}&grant_type=client_credentials")
        print(r.json())
        return f"Bearer {r.json()['access_token']}"
    
    def getIdFromName(self):
        r = requests.get(f"https://api.twitch.tv/helix/users?login={self.name}", headers={"Authorization": self.accessToken, "Client-Id": self.credentials['twitch']['id']})
        return r.json()['data'][0]['id']

    def listSubscriptions(self):
        r = requests.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers={"Authorization": self.accessToken, "Client-Id": self.credentials['twitch']['id']})
        return r.json()
    
    def deleteSubscription(self, sub_id):
        r = requests.delete(f"https://api.twitch.tv/helix/eventsub/subscriptions?id={sub_id}", headers={"Authorization": self.accessToken, "Client-Id": self.credentials['twitch']['id']})
        print(r)

    def createEventSub(self):
        headers = {
            "Authorization": self.accessToken,
            "Client-Id": self.credentials['twitch']['id'],
            "Content-Type": "application/json"
        }
        data = {
            "type": "channel.follow",
            "version": "1",
            "condition": {
                "broadcaster_user_id": self.userId
            },
            "transport": {
                "method": "webhook",
                "callback": self.credentials['endpoint'],
                "secret": self.credentials['twitch']['eventsub_secret']
            }
        }
        r = requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers, data=json.dumps(data))
        print(r.json())

def registerUser(username):
    eventSubInstance = registerEventsub(username)
    eventSubInstance.createEventSub()

def removeSubscriptions():
    eventSubInstance = registerEventsub()
    for item in eventSubInstance.listSubscriptions()['data']:
        eventSubInstance.deleteSubscription(item['id'])

def listSubscriptions():
    eventSubInstance = registerEventsub()
    print(json.dumps(eventSubInstance.listSubscriptions()['data'], indent=4))
    
