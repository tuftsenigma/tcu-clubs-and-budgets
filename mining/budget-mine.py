import 	sys
import 	os
import	re
import 	json
import	xlrd
import 	xlwt
import 	pandas as pd
from 	tuftstrendstools 	import *
from	commands			import getoutput


if __name__ == "__main__":
	"""
		Parse local budget xls files, extract data and upload
		back to DB. 	
	"""

	DB = TrendsDB()
	orgsCllxn = DB.getCllxn("TuftsOrgs")
	clubs = orgsCllxn.find()

	# extract expense data
	expense_file = "../data/expense_reports"
	with open(expense_file, "wb+") as f:
		for club in clubs:
			try:
				filename = "../data/budgets/" + "".join(club["name"].split()) + ".xls"
				df = pd.read_excel(filename, header=None)
			
				f.write("\n\nCLUB\t{}".format(club["name"]))
				f.write(df.tail().to_string())

				expense_data = df.tail().to_string().lower()

				net_amt = None
				total_amt = None
				for line in expense_data.split("\n"):
					if "net amount" in line:
						for word1 in line[4::].split(" "):
							if word1.isdigit():
								net_amt = word1
					if "total expenses" in line:
						for word2 in line[4::].split(" "):
							if word2.isdigit():
								total_amt = word2
					if "food expenses" in line:
						for word3 in line[4::].split(" "):
							if word3.isdigit():
								food_amt = word3					


				print "club: {}, net expenses: {},  total expenses: {}".format(club["name"][:-1], net_amt, total_amt)
				orgsCllxn.update({ "name" : club["name"] }, { "$set" : { "net_expenses" : net_amt }})
				orgsCllxn.update({ "name" : club["name"] }, { "$set" : { "total_expenses" : total_amt }})
				orgsCllxn.update({ "name" : club["name"] }, { "$set" : { "food_expenses" : food_amt }})

						#print [word for word in line.split(" ") if word != "nan" or word != ""]

			except IOError as e:
				print e

	# pull out specific numbers and push to database
	# with open(expense_file, "r") as f:
	# 	for club in clubs:
	# 		output = getoutput("grep {clubn} -A 7 {filen} | grep {field} | cut -d " " -f 14".format(clubn=club["name"], filen=expense_file, field="Total Expenses"))
	# 		print "Club: {}, Total Expenses: {}".format(club["name"], output) 	

