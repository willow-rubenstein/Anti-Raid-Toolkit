import requests 
import json

class eventSubListener:
    def __init__(self):
        self.credentials = json.load(open('credentials.json'))