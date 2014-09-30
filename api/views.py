import json, calendar, urlparse, hashlib, datetime
from django.views.decorators.http import require_http_methods
from django.http import *

import settings
from models import *

@require_http_methods(["GET"])
def index(request):
    response = {"version":settings.MEMEX_API_VERSION}
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["POST"])
def get_urlkey(request, fmt):
    response = None
    status = 200
    content_type = None
    urlkey = None
    try:
        url = request.body
        try:
            url = json.loads(request.body)
        except:
            pass
        url_hash = hashlib.sha1(url).hexdigest()
        url_parts = urlparse.urlsplit(url)
        domain_path = url_parts.hostname.split('.')
        domain_path.reverse()
        urlkey = "{0}_{1}".format("_".join(domain_path), url_hash)
    except:
        status = 400
        urlkey = ''
    if fmt == "txt" or fmt is None:
        content_type = "text/plain"
        response = urlkey
    elif fmt == "json":
        response = json.dumps({'urlkey':urlkey})
        content_type="application/json"
    else:
        content_type = "text/plain"
        status = 400
        response = ''
    return HttpResponse(response, content_type=content_type, status=status)

@require_http_methods(["GET"])
def get_timestamp(request, fmt):
    response = None
    status = 200
    content_type = None
    urlkey = None
    timestamp = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
    if fmt == "txt" or fmt is None:
        content_type = "text/plain"
        response = timestamp
    elif fmt == "json":
        response = json.dumps({'timestamp':timestamp})
        content_type="application/json"
    else:
        content_type = "text/plain"
        status = 400
        response = ''
    return HttpResponse(response, content_type=content_type, status=status)

@require_http_methods(["GET"])
def scan_timestamps(request):
    limit = request.REQUEST.get("limit", 1000)
    expand = request.REQUEST.get("expand", False)
    result = TimestampIndex.scan(limit=limit, expand=expand)
    return HttpResponse(json.dumps(result), content_type="application/json")

@require_http_methods(["GET"])
def search_by_timestamp(request, start = None, stop = None):
    limit = request.REQUEST.get("limit", 1000)
    expand = request.REQUEST.get("expand", False)
    if stop is None:
        stop = str(calendar.timegm(datetime.datetime.utcnow().utctimetuple()))
    result = TimestampIndex.scan(start, stop, limit, expand)
    return HttpResponse(json.dumps(result), content_type="application/json")

@require_http_methods(["GET"])
def search_by_attribute(request, attribute, value):
    limit = request.REQUEST.get("limit", 1000)
    expand = request.REQUEST.get("expand", False)
    result = AttributeIndex.scan(attribute, value, limit, expand)
    return HttpResponse(json.dumps(result), content_type="application/json")

@require_http_methods(["GET", "POST"])
def urlkey_list(request, urlkey, start, stop):
    if request.method == "GET":
        limit = request.REQUEST.get("limit", 1000)
        expand = request.REQUEST.get("expand", False)
        if stop is None:
            stop = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
        result = Artifact.scan(urlkey, start, stop, limit, expand)
        if result is None:
            return HttpResponseNotFound(json.dumps({"error":"not found", "debug":urlkey}))
        return HttpResponse(json.dumps(result, indent=2), content_type="application/json")
    elif request.method == "POST":
        data = json.loads(request.body)
        timestamp = calendar.timegm(datetime.datetime.utcnow().utctimetuple())
        result = Artifact.put(urlkey, timestamp, data["data"])
        return HttpResponse(json.dumps({"result":result, "timestamp":timestamp}), content_type="application/json")

@require_http_methods(["GET", "PUT"])
def urlkey_item_attribute(request, urlkey, timestamp, attribute):
    if request.method == "GET":
        item = Attribute.get("{0}_{1}".format(urlkey, timestamp), attribute)
        if item is None:
            return HttpResponseNotFound(json.dumps({"error":"not found"}))
        return HttpResponse(item, content_type="application/json")
    elif request.method == "PUT":
        data = request.body
        result = Attribute.put("{0}_{1}".format(urlkey, timestamp), attribute, data)
        return HttpResponse(json.dumps(result), content_type="application/json")

@require_http_methods(["GET", "PUT"])
def urlkey_item(request, urlkey, timestamp):
    if request.method == "GET":
        item = Artifact.get(urlkey, timestamp)
        if item is None:
            return HttpResponseNotFound(json.dumps({"error":"not found"}))
        return HttpResponse(json.dumps(item, indent=2), content_type="application/json")
    elif request.method == "PUT":
        data = json.loads(request.body)
        result = Artifact.put(urlkey, timestamp, data["data"])
        return HttpResponse(json.dumps({"result":result}), content_type="application/json")
