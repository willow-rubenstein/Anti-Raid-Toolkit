from websocket import create_connection
from threading import Thread
import json

botNames = ['hoss', 'host', 'zachsapttv', 'zachsaptv']
credentials = json.load(open('credentials.json'))
irc = credentials['irc']

def banUser(username, broadcaster_name):
    print(f"User follower event recieved for {broadcaster_name} (username: {username})")
    ws = create_connection('wss://irc-ws.chat.twitch.tv')
    ws.send(f"PASS {irc}")
    ws.send(f'NICK hateraidsbgone')
    ws.send(f"PRIVMSG #{broadcaster_name} :/ban {username}")
    ws.close()

def banAlgorithm(feed):
    eventData = feed['event']
    failedChecks = 0
    for item in botNames:
        if eventData['user_login'].find(item) != -1:
            failedChecks += 1
    if failedChecks > 0:
        Thread(target=banUser, args=(eventData['user_login'], eventData['broadcaster_user_login'],)).start()   