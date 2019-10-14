#!/bin/env python

import optparse
import mapbox
from copy import deepcopy
import unicodecsv as csv

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
		print("Usage: python geocode.py --input [csv] --output [csv]")
		exit(1)

	infile = open(options.input, 'rb')
	reader = csv.reader(infile)

	outfile = open(options.output, 'wb')
	writer = csv.writer(outfile)

	skipped = 0
	errors = 0
	geocoded = 0

	row_num = 0
	headers = []
	new_headers = []

	for row in reader:

		row_num = row_num + 1

		if row_num == 1:
			headers = row
			new_headers = deepcopy(headers)
			new_headers.insert(0, 'longitude')
			new_headers.insert(0, 'latitude')
			writer.writerow(new_headers)
			continue

		record = csv_row(row, headers)

		school = record["SCHOOL"]
		address = record["Address"]
		city = record["City"]
		state = record["State"]
		zip = record["Zip"]

		if not address:
			skipped = skipped + 1
			continue

		query = "%s, %s, %s %s" % (address, city, state, zip)

		rsp = mapbox.geocode(query)

		if not "features" in rsp or len(rsp["features"]) == 0:
			errors = errors + 1
			continue

		first = rsp["features"][0]

		if not 'center' in first:
			errors = errors + 1
			continue

		lat = first['center'][1]
		lng = first['center'][0]

		row.insert(0, lng)
		row.insert(0, lat)

		writer.writerow(row)

		geocoded = geocoded + 1

		print("%s: %f, %f" % (school, lat, lng))

	print("geocoded: %d" % geocoded)
	print("skipped: %d" % skipped)
	print("errors: %d" % errors)
	print("done")
