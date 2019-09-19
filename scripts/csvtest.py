import csv

with open('SupermarketDB.csv', 'wb') as csvfile:
	db = csv.writer(csvfile, delimiter=' ')
	db.writerow(['24019189112','0'])
	db.writerow(['32128254112', '0'])
