#!/bin/env python

import us, json
import unicodecsv as csv
import helpers

if __name__ == '__main__':

	data = {
		'title': 'Days lost due to discipline per 100 students',
		'counties': {},
		'states': {}
	}

	ignore_counties = []
	file = open('%s/sources/map_b_ignore.csv' % helpers.root_dir(), 'rb')
	reader = csv.reader(file)

	row_num = 0
	headers = []

	for row in reader:
		row_num = row_num + 1

		if row_num == 1:
			headers = row
			continue

		record = helpers.csv_row(row, headers)
		if record["Remove County from CNC Map"] == "1":
			ignore_counties.append(record["county_geoid"])

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

		if geoid in ignore_counties:
			continue

		if geoid == 'Grand Total':
			continue

		geoid = geoid.zfill(5)

		data['counties'][geoid] = {
			'all': helpers.single_digit(record['All Student Days Lost per 100 Students']),
			'black': helpers.single_digit(record['Black Days Lost per 100 Students']),
			'latino': helpers.single_digit(record['Latino Days Lost per 100 Students']),
			'white': helpers.single_digit(record['White Days Lost per 100 Students']),
			'native_american': helpers.single_digit(record['Native American Days Lost per 100 Students']),
			'pacific_islander': helpers.single_digit(record['Pac. Islander Lost per 100 Students']),
			'asian': helpers.single_digit(record['Asian Days Lost per 100 Students'])
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
			'all': helpers.single_digit(record['All Students per 100']),
			'black': helpers.single_digit(record['Black Students per 100']),
			'latino': helpers.single_digit(record['Latino Students per 100']),
			'white': helpers.single_digit(record['White Students per 100']),
			'native_american': helpers.single_digit(record['Native American Students per 100']),
			'pacific_islander': helpers.single_digit(record['Pac. Islander Students per 100']),
			'asian': helpers.single_digit(record['Asian Students per 100'])
		}

	root_dir = helpers.root_dir()
	file = open('%s/data/map_b.json' % root_dir, 'wb')
	json.dump(data, file, sort_keys=True)
