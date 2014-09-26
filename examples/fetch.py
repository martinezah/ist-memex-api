#!/usr/bin/env python
import requests, urlparse, hashlib, calendar, sys, json, re, os
from datetime import datetime

API_BASE_URL = os.environ.get('API_BASE_URL', "http://127.0.0.1:8000/")

def submit_url(url, timestamp, response_body, status = 200, request_headers = [], response_headers = [], method = "GET", request_body = None):
    data = {
        "url": url,
        "timestamp": timestamp,
        "method": method,
        "status": status,
        "headers": {
            "request" : request_headers,
            "response" : response_headers,
        },
        "response" : response_body,
        "request" : request_body,
    }
    key = create_url_key(url, timestamp)
    api_key_url = "{0}{1}{2}/".format(API_BASE_URL, "artifacts/", key)
    r = requests.put(api_key_url, data = json.dumps({"data":data}))
    return api_key_url
 
def put_attribute(url, timestamp, attribute, data):
    api_key_url = "{0}{1}{2}/{3}/".format(API_BASE_URL, "artifacts/", create_url_key(url, timestamp), attribute)
    r = requests.put(api_key_url, data = data.strip())
    return api_key_url

def extract_age(content):
    return re.findall("Poster's age: ([0-9]+)", content)

def extract_phone(content):
    return re.findall("\d{3}-\d{3}-\d{4}", content)

def extract_location(content):
    return re.findall("Post ID: [0-9]+ ([^<]+)<", content)
    
def create_url_key(url, timestamp, separator = "_"):
     url_hash = hashlib.sha1(url).hexdigest()
     url_parts = urlparse.urlsplit(url)
     domain_path = url_parts.hostname.split('.')
     domain_path.reverse()
     return "{0}{1}{2}{1}{3}".format(separator.join(domain_path), separator, url_hash, timestamp)

def get_url(url, headers=None):
     r = requests.get(url, headers=headers)
     ts = calendar.timegm(datetime.utcnow().utctimetuple())
     print submit_url(url, ts, r.text, r.status_code, dict(r.request.headers), dict(r.headers), r.request.method)
     parse(url, ts)

def parse(url, timestamp):
    urlkey = "{0}{1}{2}/".format(API_BASE_URL, "artifacts/", create_url_key(url, timestamp))
    r = requests.get(urlkey)
    data = json.loads(r.text)
    content = data['data']['response']

    matches = extract_phone(content)
    if matches:
        for attr in matches:
            print "phone: {0}".format(attr)
            put_attribute(url, timestamp, "phone", attr)

    matches = extract_location(content)
    if matches:
        for attr in matches:
            print "location: {0}".format(attr)
            put_attribute(url, timestamp, "location", attr)

    matches = extract_age(content)
    if matches:
        for attr in matches:
            print "age: {0}".format(attr)
            put_attribute(url, timestamp, "age", attr)
     
if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_url(sys.argv[1])
    else:
        for line in sys.stdin.readlines():
            get_url(line)
