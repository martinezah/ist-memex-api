import json, calendar, urlparse, hashlib
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.http import *

import settings
from models import *

@require_http_methods(["GET"])
def index(request):
    response = {"version":settings.MEMEX_API_VERSION}
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["POST"])
def get_urlkey(request):
    status = 200
    response = ''
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
        response = "{0}_{1}".format("_".join(domain_path), url_hash)
    except:
        status = 400
        response = ''

    return HttpResponse(response, content_type="text/plain", status=status)

@require_http_methods(["GET"])
def get_timestamp(request):
    response = calendar.timegm(datetime.utcnow().utctimetuple())
    return HttpResponse(json.dumps(response), content_type="text/plain")

@require_http_methods(["GET"])
def search_by_timestamp(request, start, stop):
    response = {"view":"search_by_timestamp"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["GET"])
def search_by_attribute(request, attribute, value):
    response = {"view":"search_by_attribute"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["GET", "POST"])
def urlkey_list(request, urlkey, start, stop):
    response = {"view":"urlkey_list"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["GET", "PUT"])
def urlkey_item_attribute(request, urlkey, timestamp, attribute):
    response = {"view":"urlkey_item_attribute"}
    return HttpResponse(json.dumps(response), content_type="application/json")

@require_http_methods(["GET", "PUT"])
def urlkey_item(request, urlkey, timestamp):
    response = {"view":"urlkey_item"}
    return HttpResponse(json.dumps(response), content_type="application/json")
