import csv
import json

csvfile = open('1.csv', 'r')
jsonfile = open('file.json', 'w')

fieldnames = ("FirstName", "LastName", "IDNumber", "Message")
reader = csv.DictReader(csvfile, fieldnames)
for row in reader:
    json.dump(row, jsonfile)
    jsonfile.write('\n')
