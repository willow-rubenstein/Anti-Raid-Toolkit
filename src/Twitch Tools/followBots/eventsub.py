import requests 
import json
from logic import logic
from threading import Thread
import time

class eventListen:
    def __init__(self):
        self.credentials = json.load(open('credentials.json'))
    
    def getEvent(self):
        r = requests.get(self.credentials['pipedream']['get_endpoint'], headers={"Authorization": self.credentials['pipedream']['token']})
        return r.json()['data']
    
    def runLogic(self):
        for item in self.getEvent():
            payload = item['event']['body']
            Thread(target=logic, args=(payload, )).start()
        self.clearEvent()

    def clearEvent(self):
        requests.delete(self.credentials['pipedream']['delete_endpoint'], headers={"Authorization": self.credentials['pipedream']['token']})

e = eventListen()
while True:
    e.runLogic()
    time.sleep(0.75)
