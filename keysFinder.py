from define import *

while True:
	print(time())
	try:
		with open(FINAL_JSON_PATH, "r") as f:
			tweets = loads(f.read())

		allWords = {}
		nbr = str(len(tweets))
		for i,tw in enumerate(tweets):
			#if i >= 100:
				#break
			#if i % 100 == 0:
				#print(str(i)+" / "+nbr + " | nbrWords "+str(len(allWords)))
			if tw["text"][0] == "R" and tw["text"][1] == "T":
				continue
			tw["text"] = tw["text"].lower()
			if tw["followers"] <= NBR_MIN_FOL_HOT:
				continue

			#BY CURRENCY



			#HOT
			sp = tw["text"].split(" ")
			for word in sp:
				#print(word + " " + str(len(word)))
				if len(word) >= 3:
					if len(word) >= 4 or word[0] == "$":
						word = word.replace("#", "").replace("@", "").replace("…", "").replace(":", "").replace(";", "").replace(".", "").replace(",", "").replace("!", "").replace("?", "")
						if not word in allWords:
							allWords[word] = 0
						lastText = ""
						for j,tww in enumerate(tweets):
							if (len(tww["text"]) < 30):
								continue
							if lastText[:20] == tww["text"][:20]:
								continue
							if tww["text"][0] == "R" and tww["text"][1] == "T":
								continue
							if i == j:
								continue
							if word+" " in tww["text"]:
								allWords[word] += 1
								#print(word)
							lastText = tww["text"]
		with open("blackKeys", "r") as f:
			a = f.read()

		bl = []
		for line in a.split("\n"):
			if line == "\n":
				continue
			bl.append(line)

		so = sorted(allWords.items(), key=operator.itemgetter(1))
		so = so[::-1]
		i = 0
		j = 0
		final = []
		while j < NBR_KEYS_HOTS:
			i += 1
			if so[i][0] in bl or len(so[i][0]) <= 3 or "http" in so[i][0]:
				continue
			j += 1
			final.append({
				"name" 	: so[i][0],
				"pop"	: so[i][1],
			})

		with open(HOT_JSON_PATH, "w") as f:
			f.write(dumps(final))
	except:
		traceback.print_exc()
	print("Done");
	sleep(TIME_RELOAD_HOT)
