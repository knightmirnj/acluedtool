#!/bin/env python

import us, json
import unicodecsv as csv
import helpers

if __name__ == '__main__':

	data = {
		'title': 'Arrests per 10,000 students',
		'states': {},
		'nation': None
	}

	file = open('%s/sources/map_d.csv' % helpers.root_dir(), 'rb')
	reader = csv.reader(file)

	row_num = 0
	headers = []

	for row in reader:
		row_num = row_num + 1

		if row_num == 1:
			headers = row
			continue

		record = helpers.csv_row(row, headers)
		abbrev = record['STATE'].lower()

		if not abbrev:
			break

		if abbrev == 'nation':
			data['nation'] = {
				'total': int(record['Arrests Total'].replace(',', '')),
				'all_per_10000': helpers.single_digit(record['Arrests per 10,000 Students']),
				'asian_per_10000': helpers.single_digit(record['Asian Arrests per 10,000 Students']),
				'black_per_10000': helpers.single_digit(record['Black Student Arrests per 10,000']),
				'latino_per_10000': helpers.single_digit(record['Latino Student Arrests per 10,000']),
				'native_american_per_10000': helpers.single_digit(record['Native American Arrests per 10,000 Students']),
				'white_per_10000': helpers.single_digit(record['White Student Arrests per 10,000']),
				'pacific_islander_per_10000': helpers.single_digit(record['Pac. Islander Arrests per 10,000 Students'])
			}
		else:
			name = us.states.lookup(abbrev).name
			geoid = us.states.lookup(abbrev).fips
			data['states'][geoid] = {
				'name': name,
				'abbrev': abbrev,
				'total': int(record['Arrests Total'].replace(',', '')),
				'all_per_10000': helpers.single_digit(record['Arrests per 10,000 Students']),
				'asian_per_10000': helpers.single_digit(record['Asian Arrests per 10,000 Students']),
				'black_per_10000': helpers.single_digit(record['Black Student Arrests per 10,000']),
				'latino_per_10000': helpers.single_digit(record['Latino Student Arrests per 10,000']),
				'native_american_per_10000': helpers.single_digit(record['Native American Arrests per 10,000 Students']),
				'white_per_10000': helpers.single_digit(record['White Student Arrests per 10,000']),
				'pacific_islander_per_10000': helpers.single_digit(record['Pac. Islander Arrests per 10,000 Students'])
			}

	root_dir = helpers.root_dir()
	file = open('%s/data/map_d.json' % root_dir, 'wb')
	json.dump(data, file, sort_keys=True)
