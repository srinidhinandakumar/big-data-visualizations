#!/bin/bash
location=$1
echo "Curling data from Solr Index"
curl -X POST -H 'Content-Type: application/json' 'http://localhost:8983/solr/ufo_data/select?q=*:*&wt=json' > $location
echo "Fetching relevant shapes"
python3 fetch_data.py $location shape
echo "Fetching relevant time and month data"
python3 fetch_data.py $location month