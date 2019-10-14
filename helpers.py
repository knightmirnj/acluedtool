#!/bin/env python

import os, re, sys
import psycopg2

def db_connect():

	db_url = os.getenv('DATABASE_URL', 'postgres://schools')
	postgres = re.search('^postgres://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)$', db_url)
	postgres_dbname = re.search('^postgres://(\w+)$', db_url)

	if postgres:
		db_vars = (
			postgres.group(5), # dbname
			postgres.group(3), # host
			postgres.group(4), # port
			postgres.group(1), # user
			postgres.group(2)  # password
		)
		db_dsn = "dbname=%s host=%s port=%s user=%s password=%s" % db_vars

	elif postgres_dbname:
		db_dsn = "dbname=%s" % postgres_dbname.group(1)

	else:
		print("Could not parse DATABASE_URL. Note: this one only works on PostGIS.")
		sys.exit(1)

	conn = psycopg2.connect(db_dsn)
	return conn

def root_dir():
	script = os.path.realpath(sys.argv[0])
	scripts_dir = os.path.dirname(script)
	return os.path.dirname(scripts_dir)

def single_digit(num):
	if isinstance(num, basestring):
		num = num.replace(',', '')
		if not re.search('^[0-9.]+$', num):
			return None
		num = float(num)
	simple = format(num, '0.1f')
	return float(simple)

def csv_row(row, headers):
	col_num = 0
	row_obj = {}
	for key in headers:
		row_obj[key] = row[col_num]
		col_num = col_num + 1
	return row_obj
