#!/usr/bin/env python
import urlparse, hashlib, time, sys, json, re, os, socket

from requests.packages.urllib3.connectionpool import HTTPConnectionPool

# patch requests to capture IP info
def _make_request(self,conn,method,url,**kwargs):
    response = self._orig_make_request(conn,method,url,**kwargs)
    sock = getattr(conn,'sock',False)
    if sock:
        setattr(response,'peer',sock.getpeername())
    else:
        setattr(response,'peer',None)
    return response
HTTPConnectionPool._orig_make_request = HTTPConnectionPool._make_request
HTTPConnectionPool._make_request = _make_request

import requests

API_BASE_URL = os.environ.get('API_BASE_URL', "http://127.0.0.1:8000/")

SOFTWARE_DESC = "Memex Development Archiver https://github.com/istresearch/ist-memex-api"

def submit_url(url, timestamp, response_body, request_body = None, method = "GET", status = 200, request_headers = [], response_headers = [], client_hostname = None, client_ip = None, server_hostname = None, server_ip = None, robots_policy = "classic", software = SOFTWARE_DESC, contact_name = None, contact_email = None):
    data = {
        "url": url,
        "timestamp": timestamp,
        "request": {
            "method": method,
            "client": {
                "hostname": client_hostname,
                "address": client_ip,
                "software": software,
                "robots": robots_policy,
                "contact": {
                    "name": contact_name,
                    "email": contact_email,
                },
            },
            "headers": request_headers,
            "body": request_body,
        },
        "response": {
            "status": status,
            "server": {
                "hostname": server_hostname,
                "address": server_ip,
            },
            "headers": response_headers,
            "body" : response_body,
        },
    }
    key = create_url_key(url)
    api_key_url = "{0}{1}{2}/{3}".format(API_BASE_URL, "url/", key, timestamp)
    r = requests.put(api_key_url, data = json.dumps({"data":data}))
    return api_key_url
 
def put_attribute(urlkey, timestamp, attribute, data):
    api_key_url = "{0}{1}{2}/{3}/{4}".format(API_BASE_URL, "url/", urlkey, timestamp, attribute)
    r = requests.put(api_key_url, data = data.strip())
    return api_key_url

def extract_age(content):
    return re.findall("Poster's age: ([0-9]+)", content)

def extract_phone(content):
    result = []
    for match in re.findall("(\d{3})[^0-9a-zA-Z](\d{3})[^0-9a-zA-Z](\d{4})", content):
        result.append("".join(match))
    if len(result):
        return result
    return None

def extract_location(content):
    return re.findall("Post ID: [0-9]+ ([^<]+)<", content)
    
def create_url_key(url, separator = "_"):
     url_hash = hashlib.sha1(url).hexdigest()
     url_parts = urlparse.urlsplit(url)
     domain_path = url_parts.hostname.split('.')
     domain_path.reverse()
     return "{0}{1}{2}".format(separator.join(domain_path), separator, url_hash)

def get_url(url, headers=None):
     r = requests.get(url, headers=headers)
     rq = r.request
     ts = int(round(time.time() * 1000))
     myip = requests.get('http://ipecho.net/plain').text
     myfqdn = socket.getfqdn()
     remip = r.raw._original_response.peer[0]
     remfqdn = urlparse.urlsplit(url).hostname
     print submit_url(url, ts, r.text, rq.body, rq.method, r.status_code, dict(rq.headers), dict(r.headers), myfqdn, myip, remfqdn, remip)
     parse(url, ts)

def parse(url, timestamp):
    key = create_url_key(url)
    api_key_url = "{0}{1}{2}/{3}".format(API_BASE_URL, "url/", key, timestamp)
    r = requests.get(api_key_url)
    data = json.loads(r.text)
    content = data['response']['body']

    matches = extract_phone(content)
    if matches:
        for attr in matches:
            print "phone: {0}".format(attr)
            put_attribute(key, timestamp, "phone", attr)

    matches = extract_location(content)
    if matches:
        for attr in matches:
            print "location: {0}".format(attr)
            put_attribute(key, timestamp, "location", attr)

    matches = extract_age(content)
    if matches:
        for attr in matches:
            print "age: {0}".format(attr)
            put_attribute(key, timestamp, "age", attr)
     
if __name__ == "__main__":
    if len(sys.argv) == 2:
        get_url(sys.argv[1])
    else:
        for line in sys.stdin.readlines():
            get_url(line)
