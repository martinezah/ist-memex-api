use default;

drop table if exists memex_artifact_data;
create table memex_artifact_data (
    kk string,
    vv string
) stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
with serdeproperties ('hbase.columns.mapping' = ':key,f:vv')
tblproperties ('hbase.table.name' = 'memex_artifact_data');

drop table if exists memex_timestamp_artifact_index;
create table memex_timestamp_artifact_index (
    kk string,
    vv tinyint
) stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
with serdeproperties ('hbase.columns.mapping' = ':key,f:vv')
tblproperties ('hbase.table.name' = 'memex_timestamp_artifact_index');

drop table if exists memex_attribute_data;
create table memex_attribute_data (
    kk string,
    vv tinyint
) stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
with serdeproperties ('hbase.columns.mapping' = ':key,f:vv')
tblproperties ('hbase.table.name' = 'memex_attribute_data');

drop table if exists memex_attribute_artifact_index;
create table memex_attribute_artifact_index (
    kk string,
    vv tinyint
) stored by 'org.apache.hadoop.hive.hbase.HBaseStorageHandler'
with serdeproperties ('hbase.columns.mapping' = ':key,f:vv')
tblproperties ('hbase.table.name' = 'memex_attribute_artifact_index');

