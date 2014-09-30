#!/bin/bash
TABLE=$1
END=$2
START=0
CHUNK=5000

while [ "$START" -lt "$END" ] 
do
    STOP=$(($START + $CHUNK - 1))
    ./roxy_scrape.py -h roxy-db.istresearch.com -u marti -p $(cat ~/.pw) -d roxy_scrape -t $TABLE -s $START -e $STOP
    START=$((STOP + 1))
done
