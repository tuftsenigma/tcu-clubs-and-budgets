import	requests
import 	json
import 	sys
import 	os
import 	pandas
import 	xlrd
from	tuftstrendstools		import *


if __name__ == "__main__":
	"""
		Hit budgetURL of each organization and locally download xls file.
	"""

	DB = TrendsDB()
	orgsCllxn = DB.getCllxn("TuftsOrgs")
	clubs = orgsCllxn.find()

	with open("../data/fb.json") as data:
		orgData = json.load(data)["pages"]["clubs"]

	for club in clubs:
		try:
			res = requests.get(orgData[club["name"]]["budgetURL"])
			with open("../data/budgets/{}.xls".format("".join(club["name"].split())), "wb+") as f:
				f.write(res.content)

		except:
			print "..no valid budget recieved for " + club["name"]
