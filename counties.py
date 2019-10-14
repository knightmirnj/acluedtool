#!/bin/env python

import json
import helpers

if __name__ == '__main__':

	root_dir = helpers.root_dir()
	path = "%s/sources/counties.geojson" % root_dir

	print("loading %s" % path)
	file = open(path, 'rb')
	geojson = json.load(file)

	data = {}

	for feature in geojson["features"]:

		props = feature["properties"]
		geoid = props["GEOID"]
		name = props["NAME"]

		data[geoid] = name

	path = "%s/data/counties.json" % root_dir
	print("saving %s" % path)
	file = open(path, 'wb')
	json.dump(data, file, sort_keys=True)
