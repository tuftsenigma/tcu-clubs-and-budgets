import 	json
import 	sys
import	requests
import 	os
from	tuftstrendstools		import *
from	BeautifulSoup			import *



"""
Run scripts / experiments / metrics on collected TCU and organization data
"""

def print_allocations():
	"""total allocations to all clubs"""
	total_allocated = 0
	food_allocated = 0
	for c in clubs:
		try:
			if c["total_expenses"] != None:
				total_allocated += float(c["total_expenses"])
			if c["food_expenses"] != None:
				food_allocated += float(c["food_expenses"])
		except KeyError:
			continue

	print "total allocated: {}\nfood money allocated: {}\n".format(total_allocated, food_allocated)


def print_councils():
	"""total clubs per each council"""
	councils = ["cultural", "programming", "media", "religious", "performance", "service_and_miscellaneous", "pre_professional", "political", "student_government"]

	cd = {}
	for council in councils:
		cd[council] = 0
		res = requests.get("http://senate.tufts.edu/studentorganizations/{}".format(council))
		soup = BeautifulSoup(res.text)
		table = soup("table")[0]

		cd[council] = len(table.findAll("tr")) - 1
		print "{} : {}".format(council, len(table.findAll("tr")) - 1)
	
	print "\n\n\n"
	print "total:" + str(sum(cd.values()))
	for c in sorted(cd):
		print c + ":"
		print float(cd[c])/float(sum(cd.values()))


def rank_orgs():
	"""Rank(org) = w1*affluence + w2*popularity"""
	# rank by affluence
	clubs = orgsCllxn.find({ "total_expenses" : { "$exists" : True } })
	has_money = []
	for c in clubs:
		try:
			float(c["total_expenses"])
			has_money.append(c)
		except:
			print c["total_expenses"]

	ranked_by_money = sorted(has_money, key=lambda k: float(k["total_expenses"]))
	# for r in ranked_by_money:
	# 	print "club:\t{}money:\t{}\n".format(r["name"], r["total_expenses"])


	# rank by popularity
	clubs = orgsCllxn.find({ "likes" : { "$exists" : True } })
	has_likes = []
	for c in clubs:
		try:
			float(c["likes"])
			has_likes.append(c)
		except:
			print c["likes"]

	ranked_by_popularity = sorted(has_likes, key=lambda k: int(k["likes"]))
	print "\n"
	# for r in ranked_by_popularity:
	# 	print "club:\t{}likes:\t{}\n".format(r["name"].encode("utf-8"), r["likes"])


	# use rank metric
	clubs = has_money + has_likes
	w1 = 0.2
	w2 = 8.0
	has_money_and_likes = []
	for club in clubs:
		try:
			club.update({"rank" : (w1*float(club["total_expenses"]) + w2*float(club["likes"]))/1000.0})
			if club not in has_money_and_likes:
				has_money_and_likes.append(club)
		except:
			continue

	ranked_by_rank = sorted(has_money_and_likes, key=lambda k: float(k["rank"]))
	for r in reversed(ranked_by_rank):
		print "club:\t{}rank:\t{}\nmetrics:[$={},ppl={}]\n".format(r["name"].encode("utf-8"), float(r["rank"]), r["total_expenses"], r["likes"])






if __name__ == '__main__':

	DB = TrendsDB()
	orgsCllxn = TrendsDB().getCllxn("TuftsOrgs")
	clubs = orgsCllxn.find()

	rank_orgs()
	# print_allocations()
	# print_councils()
