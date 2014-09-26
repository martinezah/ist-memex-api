from django.http import *
from models import *
import settings
import json

def index(request):
    return HttpResponse(json.dumps({"version":settings.MEMEX_API_VERSION}), content_type="application/json")

def artifact_item(request, url):
    if request.method == "PUT":
        data = json.loads(request.body)
        result = Artifact.put(url, data["data"])
        return HttpResponse(json.dumps(result), content_type="application/json")
    elif request.method == "GET":
        obj = Artifact.get(url)
        if obj is None:
            return HttpResponseNotFound(json.dumps({"error":"not found"}))
        return HttpResponse(json.dumps(obj, indent=2), content_type="application/json")
    return HttpResponseNotAllowed(["GET","PUT"], json.dumps({"error":"method not allowed"}))

def attribute_item(request, url, attribute):
    if request.method == "PUT":
        data = request.body
        result = Attribute.put(url, attribute, data)
        return HttpResponse(json.dumps(result), content_type="application/json")
    elif request.method == "GET":
        obj = Attribute.get(url, attribute)
        if obj is None:
            return HttpResponseNotFound(json.dumps({"error":"not found"}))
        return HttpResponse(obj, content_type="application/json")
    return HttpResponseNotAllowed(["GET","PUT"], json.dumps({"error":"method not allowed"}))

def attribute_scan(request, attribute, value):
    if request.method == "GET":
        result = AttributeIndex.scan(attribute, value)
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponseNotAllowed(["GET"], json.dumps({"error":"method not allowed"}))


def timestamp_scan(request, start, end = None):
    if request.method == "GET":
        result = TimestampIndex.scan(start, end)
        return HttpResponse(json.dumps(result), content_type="application/json")
    return HttpResponseNotAllowed(["GET"], json.dumps({"error":"method not allowed"}))

