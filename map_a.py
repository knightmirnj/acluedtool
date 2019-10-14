#!/bin/env python

import us, json
import unicodecsv as csv
import helpers

if __name__ == '__main__':

	data = {
		'title': 'Students attending schools that reported having cops but no counselors',
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

		if record['Remove from CNC Map'] == 1:
			continue

		if geoid == 'Grand Total' or geoid == '':
			continue

		geoid = geoid.zfill(5)

		percent = record['Percent of Schools w Cops and No Counselors']
		percent = percent.replace('%', '')

		data['counties'][geoid] = {
			'percent_cop_no_counselor': helpers.single_digit(percent),
			'students_to_cops': helpers.single_digit(record['LEO-to-Student Ratio']),
			'students_to_counselors': helpers.single_digit(record['Counselor-to-Student Ratio']),
			'students_to_social_workers': helpers.single_digit(record['SW-to-Student Ratio']),
			'students_to_psychologists': helpers.single_digit(record['Psych-to-Student Ratio']),
			'students_to_nurses': helpers.single_digit(record['Nurse-to-Student Ratio']),
			'students_to_teachers': helpers.single_digit(record['Teacher-to-Student Ratio'])
		}

	file = open('%s/sources/supports.csv' % helpers.root_dir(), 'rb')
	reader = csv.reader(file)

	row_num = 0
	headers = []

	for row in reader:
		row_num = row_num + 1

		if row_num == 1:
			headers = row
			continue

		record = helpers.csv_row(row, headers)

		state = record['STATE'].lower()

		if not us.states.lookup(state):
			continue

		geoid = us.states.lookup(state).fips
		name = us.states.lookup(state).name

		if state == 'NATION':
			continue

		percent = record['% of Students in Schools with Cops, No Counselor']
		percent = percent.replace('%', '')

		data['states'][geoid] = {
			'name': name,
			'abbrev': state,
			'percent_cop_no_counselor': helpers.single_digit(percent),
			'students_to_cops': helpers.single_digit(record['Law Enforcement-to-Students Ratio']),
			'students_to_counselors': helpers.single_digit(record['Student-to-Counselor Ratio']),
			'students_to_social_workers': helpers.single_digit(record['Student-to-Social Worker Ratio']),
			'students_to_psychologists': helpers.single_digit(record['Student-to-Psychologist Ratio']),
			'students_to_nurses': helpers.single_digit(record['Student-to-Nurse Ratio']),
			'students_to_teachers': helpers.single_digit(record['Student-to-Teachers Ratio'])
		}

	root_dir = helpers.root_dir()
	file = open('%s/data/map_a.json' % root_dir, 'wb')
	json.dump(data, file, sort_keys=True)
