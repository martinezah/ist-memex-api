#!/usr/bin/env python
from api.models import *
from time import gmtime, strftime
import sys

def format_key(key):
    keyparts = key.split("__")
    return "{0}_{1}".format(keyparts[1], flip_ts(keyparts[0]))

if __name__ == "__main__":
    ii = 0

    kwargs = {}
    if len(sys.argv) > 1:
        newer_than = sys.argv[1] 
        kwargs['row_stop'] = str(int(flip_ts(newer_than)) + 1)
    scanner = TimestampIndex.get_scanner(**kwargs)
    for kk, vv in scanner:
        ii += 1
        if ii % 100 == 0:
            print "{0} {1}: {2}".format(strftime("%H:%M:%S", gmtime()), str(ii).rjust(10), format_key(kk))

