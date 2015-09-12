import 	json
import 	sys
import 	re
import	pandas			as pd
import 	time
import 	requests
from	tuftstrendstools 	import *
from 	BeautifulSoup 		import *


DB = TrendsDB() 

# Access credentials
accessToken = "875920362459105|eBvdBjaUO_dLV9A6tN55U9B5R7w"

# Tufts data lookup
with open("../data/fb.json") as data:
	TuftsFB = json.load(data)


# Data keys
FBKeys = [
"id", 
"status_type", 
"from", 
"privacy", 
"actions", 
"update_time", 
"comments",
"created_time",
"message",
"type"
]



"""SCRAPE TCU PAGE
"""
def scrapeTCU():
	"""scrape student organizations off TCU page - query FB graph for pages and then
	load into DB"""
	councils = ["cultural", "programming", "media", "religious", "performance", "service_and_miscellaneous", "pre_professional", "political", "student_government"]
	for council in councils:
		res = requests.get("http://senate.tufts.edu/studentorganizations/{}".format(council))
		soup = BeautifulSoup(res.text)
		table = soup("table")[0]
		for i,row in enumerate(table.findAll("tr")):
			if i != 0: # first index is table header

				# name and budget file
				clubname = " ".join(filter(lambda a: a != "", row.findAll("td")[1].string.encode('utf-8').strip("\n").split(" ")))
				p = re.compile(r'\([^)]*\)')
				clubname = re.sub(p, "", clubname)
				budget_url = row.findAll("td")[2].findAll("a")[0]["href"].encode('utf-8')
				print "CLUB: {}, BUDGET AT: {}".format(clubname, budget_url)

				# search for affiliated facebook group
				fbData = searchForPage("Tufts" + clubname)
				if (fbData):
					# print json.dumps(fbData, indent=4, sort_keys=True)
					try:
						fid = fbData["data"][0]["id"]
						print fid
					except:
						print "No valid FB page id for {}".format(clubname)
						fid = ""

				# update json file
				TuftsFB["pages"]["clubs"][clubname] = {
					"budgetURL" : budget_url,
					"council" :  council,
					"FBid" : fid
				}

	with open("../data/fb.json", "w+") as outfile:
		json.dump(TuftsFB, outfile, indent=4)


def mineTCU():
	"""take organizations / ids in 'fb.json' and upload FB graph data into new cllxn"""

	global accessToken, DB

	orgsCllxn = DB.getCllxn("TuftsOrgs")

	# loop through clubs and mine data
	with open("../data/fb.json") as data:
		TuftsFB = json.load(data)

	for org in TuftsFB["pages"]["clubs"]:
		if (TuftsFB["pages"]["clubs"][org]["FBid"] != ""):
			url = "https://graph.facebook.com/{id}?access_token={token}".format(id=TuftsFB["pages"]["clubs"][org]["FBid"], token=accessToken)
			res = requests.get(url).json()

			try:
				desc = res["about"]
			except KeyError:
				desc = ""
				continue
			print res["likes"]

			# eventsUrl = "https://graph.facebook.com/{id}?fields=events&access_token={token}".format(id=TuftsFB["pages"]["clubs"][org]["FBid"], token=accessToken)
			# eventsRes = requests.get(eventsUrl).json()
			# print json.dumps(eventsRes, indent=4)

			dataObj = {
				"name" : org,
				"fbid" : TuftsFB["pages"]["clubs"][org]["FBid"],
				"council" : TuftsFB["pages"]["clubs"][org]["council"],
				"likes" : res["likes"],
				"desc" : res["about"]
			}

			orgsCllxn.insert(dataObj)




if __name__ == '__main__':
	if len(sys.argv) > 1:
		try:
			srcs = sys.argv[1::]
		except ValueError:
			print 'Invalid input... try again.'
	else:
		try:
			srcs = raw_input('Enter "scrape-tcu" OR "mine-tcu":\n').split(' ')
		except:
			print 'Invalid input... try again.'

	if srcs[0] == 'scrape-tcu':
		scrapeTCU()
	elif srcs[0] == 'mine-tcu':
		mineTCU()

