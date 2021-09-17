import requests
import json

r = requests.post("https://jcbotkm351.execute-api.us-east-2.amazonaws.com/beta", data=json.dumps({"testing": "test"}))
print(r.json())    