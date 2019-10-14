all: geocoded.csv \
     encountied.csv

schools.csv:
	ssconvert schools.xlsx schools.csv

map_a_ignore.csv:
	ssconvert map_a_ignore.xlsx map_a_ignore.csv

map_b_ignore.csv:
	ssconvert map_b_ignore.xlsx map_b_ignore.csv

geocoded.csv:
	python ../scripts/geocode.py -i schools.csv -o geocoded.csv

encountied.csv:
	python ../scripts/encounty.py -i geocoded.csv -o encountied.csv

counties.geojson:
	mkdir -p counties
	curl -o counties/counties.zip https://www2.census.gov/geo/tiger/TIGER2017/COUNTY/tl_2017_us_county.zip
	unzip -d counties counties/counties.zip
	ogr2ogr -f GeoJSON -t_srs crs:84 counties.geojson counties/tl_2017_us_county.shp
	rm -rf counties/
