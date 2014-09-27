import sys, cbor, happybase, re
import settings

class Artifact():

    @staticmethod
    def get(urlkey, timestamp):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        artifact_key = '{0}_{1}'.format(urlkey, timestamp)
        row = table.row(artifact_key)
        data = {'key': artifact_key, 'data': cbor.loads(row['f:vv']), 'attributes' : Attribute.scan(artifact_key)}
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
    def scan(prefix, start, end, limit = 1000, expand = False):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "artifact_data"))
        result = []
        if end is None:
            end = start + 1
        else:
            end = end + 1
        for artifact_key, row in table.scan(row_start = "{0}_{1}".format(prefix, start), row_stop = "{0}_{1}".format(prefix, end), limit = limit):
            data = artifact_key
            if expand:
                data = {'key': artifact_key, 'data': cbor.loads(row['f:vv']), 'attributes' : Attribute.scan(artifact_key)}
            result.append(data)

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
        table.put('{0}__{1}'.format(timestamp, urlkey, {'f:vv':'1'})
        return True

    @staticmethod 
    def scan(start, end, limit = 1000, expand = False):
        connection = happybase.Connection(settings.HBASE_HOST)
        table = connection.table('{0}{1}'.format(settings.HBASE_PREFIX, "timestamp_artifact_index"))
        result = []
        if end is None:
            end = start + 1
        else:
            end = end + 1
        for kk, vv in table.scan(row_start = start, row_stop = end, limit = limit):
            data = kk.split('__')
            artifact_key = '{0}_{1}'.format(data[1], data[0])
            if expand:
                result.append(Artifact.get(artifact_key))
            else:
                result.append(artifact_key)
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
        for kk, vv in table.scan(row_prefix='{0}__{1}__'.format(attribute, value), limit = limit):
            data = kk.split('__')
            artifact_key = data[2]
            if expand:
                result.append(Artifact.get(artifact_key))
            else:
                result.append(artifact_key)
        return result
