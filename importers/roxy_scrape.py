#!/usr/bin/env python
import MySQLdb, calendar, datetime, os, getopt, sys, urlparse, hashlib, json
from api.models import *

API_BASE_URL = os.environ.get('API_BASE_URL', "http://127.0.0.1:8000/")

def parse_options():
    options = {}
    opts, args = getopt.getopt(sys.argv[1:], 'h:u:d:p:t:s:e:') #, [ 'host=', 'user=', 'database=', 'password=', 'table=' 'start=', 'end=' ])   
    for opt,arg in opts:
        if opt in ('-h', '--host'):
            options['host'] = arg
        if opt in ('-u', '--user'):
            options['user'] = arg
        elif opt in ('-d', '--database'):
            options['database'] = arg
        elif opt in ('-p', '--password'):
            options['password'] = arg
        elif opt in ('-t', '--table'):
            options['table'] = arg
        elif opt in ('-s', '--start'):
            options['start'] = arg 
        elif opt in ('-e', '--end'):
            options['end'] = arg 
    return options

def create_url_key(url):
     url_hash = hashlib.sha1(url).hexdigest()
     url_parts = urlparse.urlsplit(url)
     domain_path = url_parts.hostname.split('.')
     domain_path.reverse()
     return "{0}_{1}".format("_".join(domain_path), url_hash)

if __name__ == "__main__":
    try:
        options = parse_options()
    except ValueError:
        sys.stderr.write("usage: {0} -h hostname -u user -d database -p password -t table -s start_id -c count\n".format(sys.argv[0]))
        exit(1)
    db = MySQLdb.connect(options['host'], options['user'], options['password'], options['database'])
    with db:
        sql = "SELECT id, url, headers AS response_headers, body, status, timestamp FROM {0} WHERE id >= {1} AND id <= {2}".format(options['table'], options['start'], options['end'])
        sys.stderr.write("{0}\n".format(sql))
        cursor = db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        for row in rows:
            urlkey = create_url_key(row[1])
            timestamp = calendar.timegm(row[5].utctimetuple())
            data = {
                "url": row[1],
                "method": "GET",
                "status": row[4],
                "headers": {
                    "request": None,
                    "response": row[2],
                },
                "request": None,
                "response": row[3],
            }
            Artifact.put(urlkey, timestamp, data)
            if (row[0] % 100 == 0):
                sys.stderr.write("{0}: {1}/{2}\n".format(row[0], urlkey, timestamp))

