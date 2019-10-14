#!/bin/env python

import os, requests, urllib

def geocode(address):

	api_key = os.getenv('MAPBOX_API_KEY', None)

	if not api_key:
		throw("no api_key defined")

	base_url = "https://api.mapbox.com"
	query = "%s.json" % urllib.quote_plus(address)
	endpoint = "/geocoding/v5/mapbox.places/%s" % query
	url = "%s%s?access_token=%s" % (base_url, endpoint, api_key)

	rsp = requests.get(url)

	return rsp.json()
