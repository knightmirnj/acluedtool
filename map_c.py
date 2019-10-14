#!/bin/env python

import us, json
import unicodecsv as csv
import helpers

if __name__ == '__main__':

	data = {
		'title': 'Days lost due to discipline for students with disabilities',
		'counties': {},
		'states': {}
	}

	file = open('%s/sources/county.csv' % helpers.root_dir(), 'rb')
	reader = csv.reader(file)

	row_num = 0
	headers = []

	for row in reader:
		row_num = row_num + 1

		if row_num == 1:
			headers = row
			continue

		record = helpers.csv_row(row, headers)

		geoid = record['CountyGeo']

		if geoid == 'Grand Total':
			continue

		geoid = geoid.zfill(5)

		data['counties'][geoid] = {
			'swd': helpers.single_digit(record['SWD Days Lost per 100 Students']),
			'swod': helpers.single_digit(record['SWoD Days Lost per 100 Students'])
		}

	file = open('%s/sources/days_lost.csv' % helpers.root_dir(), 'rb')
	reader = csv.reader(file)

	row_num = 0
	headers = []

	for row in reader:
		row_num = row_num + 1

		if row_num == 1:
			headers = row
			continue

		record = helpers.csv_row(row, headers)

		state = record['state'].lower()

		if state == 'NATION':
			continue

		if not us.states.lookup(state):
			continue

		geoid = us.states.lookup(state).fips
		name = us.states.lookup(state).name

		data['states'][geoid] = {
			'name': name,
			'abbrev': state,
			'swd': helpers.single_digit(record['Students w/ Disabilities per 100']),
			'swod': helpers.single_digit(record['Students w/o Disabilities per 100'])
		}

	root_dir = helpers.root_dir()
	file = open('%s/data/map_c.json' % root_dir, 'wb')
	json.dump(data, file, sort_keys=True)
