#!/bin/bash
TABLE=$1
START=$2
END=$3
CHUNK=1000

while [ "$START" -lt "$END" ] 
do
    STOP=$(($START + $CHUNK - 1))
    ./roxy_scrape.py -h roxy-db.istresearch.com -u marti -p $(cat ~/.pw) -d roxy_scrape -t $TABLE -s $START -e $STOP
    START=$((STOP + 1))
done
