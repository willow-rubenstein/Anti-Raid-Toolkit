import requests
import json
from os import path

file_path = path.abspath(__file__) # full path of your script
dir_path = path.dirname(file_path)
credentials_path = path.join(dir_path,'credentials.json')

class registerEventsub:
    def __init__(self, name):
        self.name = name
        self.credentials = json.load(open(credentials_path))
        self.accessToken = self.getToken()
        self.userId = self.getIdFromName()
    
    def getToken(self):
        r = requests.post(f"https://id.twitch.tv/oauth2/token?client_id={self.credentials['id']}&client_secret={self.credentials['secret']}&grant_type=client_credentials")
        return f"Bearer {r.json()['access_token']}"
    
    def getIdFromName(self):
        r = requests.get(f"https://api.twitch.tv/helix/users?login={self.name}", headers={"Authorization": self.accessToken, "Client-Id": self.credentials['id']})
        return r.json()['data'][0]['id']

    def listSubscriptions(self):
        r = requests.get("https://api.twitch.tv/helix/eventsub/subscriptions", headers={"Authorization": self.accessToken, "Client-Id": self.credentials['id']})
        return r.json()
    
    def deleteSubscription(self, sub_id):
        r = requests.delete(f"https://api.twitch.tv/helix/eventsub/subscriptions?id={sub_id}", headers={"Authorization": self.accessToken, "Client-Id": self.credentials['id']})
        print(r)

    def createEventSub(self):
        headers = {
            "Authorization": self.accessToken,
            "Client-Id": self.credentials['id'],
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
                "callback": "https://jcbotkm351.execute-api.us-east-2.amazonaws.com/beta",
                "secret": self.credentials['webhook-secret']
            }
        }
        r = requests.post("https://api.twitch.tv/helix/eventsub/subscriptions", headers=headers, data=json.dumps(data))
        print(r.json())

def registerUser(username):
    eventSubInstance = registerEventsub(username)
    eventSubInstance.createEventSub()

registerUser('nyanners')