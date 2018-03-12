# -*- coding: utf-8 -*-
from define import *

def getKeys():
	final = []
	with open(KEY_PATH, "r") as f:
		res = f.read().split("\n")
	for cur in res:
		if cur != "":
			final.append(cur.lower())
	return final

def getJsonCache():
	with open(FINAL_JSON_PATH ,"r") as f:
		return loads(f.read())

jsonCache = getJsonCache()

keys = getKeys()

def pre_send_data(cl, actData):
	server.send_message(cl, actData)
	cl["ended"] = True;

def isSpam(text):
	pass

class Listener(StreamListener):
	def on_data(self, data):
		global nbrForCache
		global act
		global actData
		global nbrForPing
		global lastTweetTime

		lastTweetTime = time()
		try:
			res = loads(data)
			act = time()
			rt = False
			if not "text" in res:
				return True
			if isSpam(res["text"]):
				pass
			if (res["text"][0] == "R" and res["text"][1] == "T"):
				rt = True;
			urls = []
			for url in res["entities"]["urls"]:
				urls.append(url["expanded_url"])
			actData = dumps({
				"text" 		: res["text"],
				"followers"	: res["user"]["followers_count"],
				"name" 		: res["user"]["name"],
				"location"	: res["geo"],
				"rt"		: rt,
				"urls"		: urls,
			})
			jsonCache.insert(0, loads(actData))
			if len(jsonCache) >= MAX_POST:
				jsonCache.pop()
			nbrForCache += 1
			if nbrForCache >= NBR_CACH_ACT:
				with open(FINAL_JSON_PATH, "w") as f:
					f.write(dumps(jsonCache))
				nbrForCache = 0
			for cl in clients.values():
				if  not cl["ended"]:
					continue
				cl["ended"] = False
				tr = threading.Thread(target=pre_send_data, args=(cl, actData))
				tr.start()
		except:
			traceback.print_exc()
		return True
	def on_error(self, status):
		print(status)

class Main:

	def startIt(self):
		while True:
			try:
				self.listener = Listener()
				self.auth = OAuthHandler(ckey, csecret)
				self.auth.set_access_token(atoken, asecret)
				self.twitterStream = Stream(self.auth, self.listener)
				self.twitterStream.filter(track=keys)
			except:
				print(C_FAIL)
				traceback.print_exc()
				print(C_RESET)
			sleep(0.5)

	def __init__(self,server):
		self.server = server
		pass

def client_left(client, server):
	try:
		clients.pop(client['id'])
		print(C_WARNING+"~~>ClientLeft	: "+client["address"][0] + "	| nbrOnline: "+str(len(clients))+C_RESET)
	except:
		pass

def new_client(client, server):
	clients[client['id']] = client
	clients[client['id']]["ended"] = True
	#print(C_OKGREEN + "new client "+ clients[client['id']]["adress"][0] +" | nbrOnline: " + str(len(clients))+ C_RESET)
	print(C_OKGREEN+"~~>NewClient	: "+client["address"][0] + "	| nbrOnline: "+str(len(clients))+C_RESET)
if __name__ == "__main__":
	server = WebsocketServer(5555, host="0.0.0.0")
	main = Main(server)
	t = threading.Thread(target=main.startIt)
	t.start()
	server.set_fn_client_left(client_left)
	server.set_fn_new_client(new_client)
	server.run_forever()
