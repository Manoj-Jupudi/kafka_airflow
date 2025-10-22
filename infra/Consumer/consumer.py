import json
import time
import boto3
from kafka import KafkaConsumer

s3 = boto3.client(
    "s3",
    endpoint_url = 'http://localhost:9002',
    aws_access_key_id= 'admin',
    aws_secret_access_key = 'password123'
)

bukcet_name = 'bronze-transactions'

consumer = KafkaConsumer(
    'stock-quotes',
    bootstrap_servers = ['localhost:29092'],
    enable_auto_commit = True,
    auto_offset_reset = 'earliest',
    group_id='bronze-C',
    value_deserializer = lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print('start')
    record = message.value
    symbol = record.get('symbol')
    ts = record.get('fetched_at',int(time.time()))
    key = f'{symbol}/{ts}.json'
    print('pushing')
    s3.put_object(
        Bucket = bukcet_name,
        Key = key,
        Body = json.dumps(record),
        ContentType = 'application/json'
    )
    print("done")