import sys, cbor, happybase, re
import settings

class Artifact():

    @staticmethod
    def get(url):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        row = table.row(url)
        data = {'key': url, 'data': cbor.loads(row['f:vv']), 'attributes' : Attribute.scan(url)}
        return data

    @staticmethod
    def put(url, data):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        table.put(url, {'f:vv':cbor.dumps(data)})
        TimestampIndex.put(url)
        return True


class Attribute():

    @staticmethod
    def get(url, attribute):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_data"))
        result = []
        for kk, vv in table.scan(row_prefix='{0}__{1}__'.format(url, attribute)):
            data = kk.split('__')
            result.append({data[1]:data[2]})
        return result

    @staticmethod
    def put(url, attribute, value):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_data"))
        table.put('{0}__{1}__{2}'.format(url, attribute, value), {'f:vv':'1'})
        AttributeIndex.put(attribute, value, url)
        return True
    
    @staticmethod
    def scan(url):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_data"))
        result = []
        for kk, vv in table.scan(row_prefix='{0}__'.format(url)):
            data = kk.split('__')
            result.append({data[1]:data[2]})
        return result

class TimestampIndex():
    @staticmethod 
    def put(url):
        data = url.split('_')
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "timestamp_artifact_index"))
        table.put('{0}__{1}'.format(data[-1], "_".join(data[:-1])), {'f:vv':'1'})
        return True

    @staticmethod 
    def scan(start, end):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "timestamp_artifact_index"))
        result = []
        for kk, vv in table.scan(row_start = start, row_stop = end):
            data = kk.split('__')
            result.append('{0}_{1}'.format(data[1], data[0]))
        return result

class AttributeIndex():
    
    @staticmethod 
    def put(attribute, value, url):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_artifact_index"))
        table.put('{0}__{1}__{2}'.format(attribute, value, url), {'f:vv':'1'})
        return True

    @staticmethod
    def scan(attribute, value):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "attribute_artifact_index"))
        result = []
        for kk, vv in table.scan(row_prefix='{0}__{1}__'.format(attribute, value)):
            data = kk.split('__')
            result.append(data[2])
        return result
