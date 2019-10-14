all: index \
     counties \
     map_a \
     map_b \
     map_c \
     map_d

index:
	python scripts/index.py -i sources/encountied.csv

counties:
	python scripts/counties.py

map_a:
	python scripts/map_a.py

map_b:
	python scripts/map_b.py

map_c:
	python scripts/map_c.py

map_d:
	python scripts/map_d.py
