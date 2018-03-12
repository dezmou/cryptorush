# -*- coding: utf-8 -*-
from 	tweepy import Stream
from 	tweepy import OAuthHandler
from 	tweepy.streaming import StreamListener
from 	json import loads, dumps
from 	time import sleep, time
import 	os
import 	asyncio
import 	datetime
import 	random
import 	websockets
import 	threading
from 	websocket_server import WebsocketServer
import 	traceback
import operator


lock 				= threading.Lock()
clients 			= {}
act 				= ""
actData 			= ""
started 			= False
jsonCache 			= []
nbrForCache 		= 0
nbrForReset 		= 0
nbrForPing 			= 0
lastTweetTime 		= time()

NBR_MIN_FOL_HOT 	= 1500
HOT_JSON_PATH 		= "./hot.json"
TIME_RELOAD_HOT 	= 60
NBR_KEYS_HOTS 		= 10
TIME_OUT 			= 10
NBR_PING 			= 50
NBR_RESET 			= 10000
NBR_CACH_ACT 		= 40
MAX_POST 			= 5000
KEY_PATH 			= "keys"
MIN_FOLOWERS 		= 0
NBR_FINAL 			= 100
FINAL_JSON_PATH 	= "/var/www/cryptorush/act.json"

C_RESET 			= '\x1b[0m'
C_HEADER 			= '\033[95m'
C_OKBLUE 			= '\033[94m'
C_OKGREEN 			= '\033[92m'
C_WARNING 			= '\033[93m'
C_FAIL 				= '\033[91m'
C_ENDC 				= '\033[0m'
C_BOLD 				= '\033[1m'
C_UNDERLINE			= '\033[4m'

ckey				="zsi623UHYEQqEOSCCPfrMX4is"
csecret				="Y6KI0wPnUuvHmBUaf1nymTI2G7sq3koRXV9Bwuuto7A9CzH7SK"
atoken				="902911147178897409-UuzuNZYG5IFoRfVCGW1nW4gy7SBgLLt"
asecret				="b9mTW0XUqJ5PeLb3hXYF1rY7AAiljRAuJISzCmU4MC24P"

def prj(s):
	try:
		print(dumps(s, indent = 4))
	except:
		traceback.print_exc()
		pass
		#print(s)
