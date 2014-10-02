import sys, cbor, happybase, re
import settings

class Artifact():

    @staticmethod
    def get(urlkey, timestamp):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        artifact_key = '{0}_{1}'.format(urlkey, timestamp) 
        row = table.row(artifact_key)
        data = cbor.loads(row['f:vv'])
        data['attributes'] = Attribute.scan(artifact_key)
        data['timestamp'] = timestamp
        data['request']['body'] = parse_unicode(data['request']['body'])
        data['response']['body'] = parse_unicode(data['response']['body'])
        return data

    @staticmethod
    def put(urlkey, timestamp, data):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        artifact_key = '{0}_{1}'.format(urlkey, timestamp)
        table.put(artifact_key, {'f:vv':cbor.dumps(data)})
        TimestampIndex.put(urlkey, timestamp)
        return True

    @staticmethod
    def put_multi(rows):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data")).batch()
        timestamps = []
        for row in rows:
            artifact_key = '{0}_{1}'.format(row['urlkey'], row['timestamp'])
            table.put(artifact_key, {'f:vv':cbor.dumps(row['data'])})
            timestamps.append({'urlkey':row['urlkey'], 'timestamp':row['timestamp']})
        table.send()
        TimestampIndex.put_multi(timestamps)
        return True

    @staticmethod
    def scan(urlkey, start, end, limit = 1000, expand = False):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        result = []
        if start is None:
            for artifact_key, row in table.scan(row_prefix="{0}_".format(urlkey), limit = int(limit)):
                if expand:
                    kk = artifact_key.split("_")
                    data = cbor.loads(row['f:vv'])
                    data['attributes'] = Attribute.scan(artifact_key)
                    data['timestamp'] = kk[-1]
                    data['request']['body'] = parse_unicode(data['request']['body'])
                    data['response']['body'] = parse_unicode(data['response']['body'])
                else:
                    data = format_artifact_key(artifact_key)
                result.append(data)
        else:
            end = str(int(end) + 1)
            for artifact_key, row in table.scan(row_start="{0}_{1}".format(urlkey, start), row_stop="{0}_{1}".format(urlkey, end), limit = int(limit)):
                if expand:
                    kk = artifact_key.split("_")
                    data = cbor.loads(row['f:vv'])
                    data['timestamp'] = kk[-1]
                    data['attributes'] = Attribute.scan(artifact_key)
                    data['request']['body'] = parse_unicode(data['request']['body'])
                    data['response']['body'] = parse_unicode(data['response']['body'])
                else:
                    data = format_artifact_key(artifact_key)
                result.append(data)
        return result

class Attribute():

    @staticmethod
    def get(artifact_key, attribute):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_data"))
        result = []
        for kk, vv in table.scan(row_prefix='{0}__{1}__'.format(artifact_key, attribute)):
            data = kk.split('__')
            result.append({data[1]:data[2]})
        return result

    @staticmethod
    def put(artifact_key, attribute, value):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_data"))
        table.put('{0}__{1}__{2}'.format(artifact_key, attribute, value), {'f:vv':'1'})
        AttributeIndex.put(attribute, value, artifact_key)
        return True
    
    @staticmethod
    def scan(artifact_key):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_data"))
        result = []
        for kk, vv in table.scan(row_prefix='{0}__'.format(artifact_key)):
            data = kk.split('__')
            result.append({data[1]:data[2]})
        return result

class TimestampIndex():

    @staticmethod 
    def put(urlkey, timestamp):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "timestamp_artifact_index"))
        table.put('{0}__{1}'.format(flip_ts(timestamp), urlkey), {'f:vv':'1'})
        return True
    
    @staticmethod
    def put_multi(rows):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "timestamp_artifact_index")).batch()
        for row in rows:
            table.put('{0}__{1}'.format(flip_ts(row['timestamp']), row['urlkey']), {'f:vv':'1'})
        table.send()
        return True

    @staticmethod 
    def scan(start = None, end = None, limit = 1000, expand = False):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "timestamp_artifact_index"))
        result = []
        if start is None:
            for kk, vv in table.scan(limit = int(limit)):
                data = kk.split('__')
                artifact_key = '{0}_{1}'.format(data[1], flip_ts(data[0]))
                if expand:
                    result.append(Artifact.get(artifact_key))
                else:
                    result.append(format_artifact_key(artifact_key))
            return result
        # else
        if end is None:
            end = start
        start = int(start) - 1
        for kk, vv in table.scan(row_start = flip_ts(end), row_stop = flip_ts(start), limit = int(limit)):
            data = kk.split('__')
            artifact_key = '{0}_{1}'.format(data[1], flip_ts(data[0]))
            if expand:
                result.append(Artifact.get(artifact_key))
            else:
                result.append(format_artifact_key(artifact_key))
        return result

class AttributeIndex():
    
    @staticmethod 
    def put(attribute, value, artifact_key):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_artifact_index"))
        table.put('{0}__{1}__{2}'.format(attribute, value, artifact_key), {'f:vv':'1'})
        return True

    @staticmethod
    def scan(attribute, value, limit = 1000, expand = False):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_artifact_index"))
        result = []
        for kk, vv in table.scan(row_prefix='{0}__{1}__'.format(attribute, value), limit = int(limit)):
            data = kk.split('__')
            artifact_key = data[2]
            if expand:
                result.append(Artifact.get(artifact_key))
            else:
                result.append(format_artifact_key(artifact_key))
        return result

def flip_ts(ts):
    flipped = []
    for cc in str(ts):
        flipped.append(str(9 - int(cc)))
    return "".join(flipped)

def format_artifact_key(artifact_key):
    kk = artifact_key.split("_")
    return "/url/{0}/{1}".format("_".join(kk[:-1]), kk[-1])

def parse_unicode(data):
    if data is not None:
        return data.decode('latin-1').encode('utf-8')
    return data
