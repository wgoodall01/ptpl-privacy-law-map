
privacy-law-data.csv: \
	data/DP.xlsx \
	data/country-data.json \
	data/region-codes.csv
	./extract-data.py > $@

data/CyberlawData.js:
	curl 'https://unctad.org/sites/default/files/data-file/CyberlawData.js' -o $@

data/WorldUnctad.js:
	curl 'https://unctad.org/themes/custom/newyork//maps/WorldUnctad.js' -o $@
	
data/DP.xlsx:
	curl 'https://unctad.org/system/files/information-document/DP.xlsx' -o $@

data/region-codes.csv:
	curl 'https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/02c8510dd9c17369abf95ecb21af9695b6bb2b37/all/all.csv' -o $@

data/country-data.json: data/CyberlawData.js
	node -e "$$(cat $<); console.log(JSON.stringify(currentData2, null, 2))" > $@

data/statistics.json: data/CyberlawData.js
	node -e "$$(cat $<); console.log(JSON.stringify(statistics, null, 2))" > $@

.PHONY: clean
clean:
	rm data/* privacy-law-data.csv
