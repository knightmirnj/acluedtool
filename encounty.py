#!/bin/env python

import optparse, os, requests, urllib
from copy import deepcopy
import unicodecsv as csv

def pip_county(lat, lng):
	base_url = "http://localhost:5000"
	endpoint = "/v1/county"
	query = "?lat=%s&lng=%s" % (lat, lng)
	url = "%s%s%s" % (base_url, endpoint, query)
	rsp = requests.get(url)
	return rsp.json()

def csv_row(row, headers):
	col_num = 0
	row_obj = {}
	for key in headers:
		row_obj[key] = row[col_num]
		col_num = col_num + 1
	return row_obj

if __name__ == '__main__':

	opt_parser = optparse.OptionParser()
	opt_parser.add_option('-i', '--input', dest='input', type='str', action='store', default=None, help='Input CSV file')
	opt_parser.add_option('-o', '--output', dest='output', type='str', default=None, action='store', help='Output CSV file')
	options, args = opt_parser.parse_args()

	if not options.input or not options.output:
		print("Usage: python encounty.py --input [csv] --output [csv]")
		exit(1)

	infile = open(options.input, 'rb')
	reader = csv.reader(infile)

	outfile = open(options.output, 'wb')
	writer = csv.writer(outfile)

	skipped = 0
	errors = 0
	encountied = 0

	row_num = 0
	headers = []
	new_headers = []

	for row in reader:

		row_num = row_num + 1

		if row_num == 1:
			headers = row
			new_headers = deepcopy(headers)
			new_headers.insert(0, 'county_geoid')
			new_headers.insert(0, 'county')
			writer.writerow(new_headers)
			continue

		record = csv_row(row, headers)

		lat = record["latitude"]
		lng = record["longitude"]

		if not lat or not lng:
			print("SKIPPED row %d" % row_num)
			skipped = skipped + 1
			continue

		rsp = pip_county(lat, lng)

		if not "county" in rsp:
			print("ERROR row %d" % row_num)
			errors = errors + 1
			continue

		county = rsp["county"]

		if not 'geoid' in county or not 'name' in county:
			print("ERROR row %d" % row_num)
			errors = errors + 1
			continue

		row.insert(0, county["geoid"])
		row.insert(0, county["name"])

		writer.writerow(row)

		encountied = encountied + 1

		print("%d. %s: %s (%s)" % (row_num, record["SCHOOL"], county["name"], county["geoid"]))

	print("encountied: %d" % encountied)
	print("skipped: %d" % skipped)
	print("errors: %d" % errors)
	print("done")
