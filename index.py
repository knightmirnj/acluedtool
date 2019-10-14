#!/bin/env python

import optparse, re
import unicodecsv as csv
import helpers

def csv_row(row, headers):
	col_num = 0
	row_obj = {}
	for key in headers:
		key = key.strip()
		row_obj[key] = row[col_num]
		col_num = col_num + 1
	return row_obj

def float_val(val):
	if val == '':
		return None
	else:
		return float(val)

if __name__ == '__main__':
	opt_parser = optparse.OptionParser()
	opt_parser.add_option('-i', '--input', dest='input', type='str', action='store', default=None, help='Input CSV file')
	options, args = opt_parser.parse_args()

	conn = helpers.db_connect()
	cur = conn.cursor()

	cur.execute("DROP TABLE IF EXISTS school CASCADE")
	cur.execute('''
	CREATE TABLE school (
		id SERIAL PRIMARY KEY,
		leaid VARCHAR(255),
		schid VARCHAR(255),
		combokey VARCHAR(255),
		name VARCHAR(255),
		latitude FLOAT,
		longitude FLOAT,
		state CHAR(2),
		county_name VARCHAR(255),
		county_geoid VARCHAR(255),
		students_enrolled INT,
		cop_no_counselor INT,
		students_to_cops FLOAT,
		students_to_counselors FLOAT,
		students_to_social_workers FLOAT,
		students_to_nurses FLOAT,
		students_to_teachers FLOAT,
		days_lost_total FLOAT,
		days_lost_per_100_students FLOAT,
		black_days_lost_per_100_students FLOAT,
		latino_days_lost_per_100_students FLOAT,
		white_days_lost_per_100_students FLOAT,
		native_american_days_lost_per_100_students FLOAT,
		pacific_islander_days_lost_per_100_students FLOAT,
		asian_days_lost_per_100_students FLOAT,
		swd_days_lost_per_100_students FLOAT,
		swod_days_lost_per_100_students FLOAT,
		arrests_referrals_per_1000_students FLOAT,
		total_arrests_referrals FLOAT,
		black_arrests_referrals_per_1000_students FLOAT,
		latino_arrests_referrals_per_1000_students FLOAT,
		white_arrests_referrals_per_1000_students FLOAT,
		native_american_arrests_referrals_per_1000_students FLOAT,
		pacific_islander_arrests_referrals_per_1000_students FLOAT,
		asian_arrests_referrals_per_1000_students FLOAT
	)
	''')

	insert_sql = '''
		INSERT INTO school (
			name,
			leaid,
			schid,
			combokey,
			latitude,
			longitude,
			state,
			county_name,
			county_geoid,
			students_enrolled,
			cop_no_counselor,
			students_to_cops,
			students_to_counselors,
			students_to_social_workers,
			students_to_nurses,
			students_to_teachers,
			days_lost_total,
			days_lost_per_100_students,
			black_days_lost_per_100_students,
			latino_days_lost_per_100_students,
			white_days_lost_per_100_students,
			native_american_days_lost_per_100_students,
			pacific_islander_days_lost_per_100_students,
			asian_days_lost_per_100_students,
			swd_days_lost_per_100_students,
			swod_days_lost_per_100_students,
			arrests_referrals_per_1000_students,
			total_arrests_referrals,
			black_arrests_referrals_per_1000_students,
			latino_arrests_referrals_per_1000_students,
			white_arrests_referrals_per_1000_students,
			native_american_arrests_referrals_per_1000_students,
			pacific_islander_arrests_referrals_per_1000_students,
			asian_arrests_referrals_per_1000_students
		) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
	'''

	if not options.input:
		print("Usage: python index.py --input [csv]")
		exit(1)

	infile = open(options.input, 'rb')
	reader = csv.reader(infile)

	row_num = 0
	headers = []

	for row in reader:

		row_num = row_num + 1

		if row_num == 1:
			headers = row
			continue

		record = csv_row(row, headers)

		cop_no_counselor = 0
		if record['Cop no Counselor'] == '1':
			cop_no_counselor = 1

		students_enrolled = record['Students Enrolled']
		if re.search('^[0-9]+$', students_enrolled):
			students_enrolled = int(students_enrolled)
		else:
			students_enrolled = None

		try:
			values = (
				record['SCHOOL'],
				record['LEAID'],
				record['SCHID'],
				record['COMBOKEY'],
				record['latitude'],
				record['longitude'],
				record['State'].lower(),
				record['county'],
				record['county_geoid'],
				students_enrolled,
				cop_no_counselor,
				float_val(record['Students-to-LEO']),
				float_val(record['Students-to-Counselors']),
				float_val(record['Student-to-Social Workers']),
				float_val(record['Students-to-Nurses']),
				float_val(record['Students-to-Teacher']),
				float_val(record['Total Days Lost']),
				float_val(record['Days Lost per 100 Students ALL']),
				float_val(record['Black Days Lost per 100 Students']),
				float_val(record['Latino Days Lost per 100 Students']),
				float_val(record['White Days Lost per 100 Students']),
				float_val(record['Native Am. Days Lost per 100 Students']),
				float_val(record['Pac. Islander Days Lost per 100 Students']),
				float_val(record['Asian Days Lost per 100 Students']),
				float_val(record['SWD Days Lost per 100 Students']),
				float_val(record['SWoD Days Lost per 100 Students']),
				float_val(record['Arrests or Referrals per 1,000']),
				float_val(record['Total # of Arrests or Referrals']),
				float_val(record['Black Arrests or Referrals per 1,000']),
				float_val(record['Latino Arrests or Referrals per 1,000']),
				float_val(record['White Arrests or Referrals per 1,000']),
				float_val(record['Native American Arrests or Referrals per 1,000']),
				float_val(record['Pac. Islander Arrests or Referrals per 1,000']),
				float_val(record['Asian Arrests or Referrals per 1,000'])
			)
		except Exception as e:
			print(str(e))
			print(record)
			break

		cur.execute(insert_sql, values)

		if row_num % 5000 == 0:
			print("indexed %d schools" % row_num)

	print("indexed %d schools" % row_num)

	conn.commit()
	print("done")
