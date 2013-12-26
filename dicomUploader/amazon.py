#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from boto.s3.connection import S3Connection
from boto.s3.bucket import Key
from boto.s3.bucket import Bucket
import boto.sqs
from boto.sqs.message import Message
import config
import ast


amazon = config.get_config_section("Amazon")

# Подключение к S3
s3conn = S3Connection(amazon['AccessKey'], amazon['SecretKey'])
bucket = Bucket(s3conn, amazon['bucket'])

# Подключение к SQS
sqsconn = boto.sqs.connect_to_region(amazon['AmazonRegion'],
                                     aws_access_key_id=amazon['AccessKey'],
                                     aws_secret_access_key=amazon['SecretKey'])
queue = sqsconn.create_queue(amazon['queue'])
print sqsconn.region


#for item in bucket.list():
#    print item.name


def put_item_to_bucket(file_path, name, storepath, metadata={}):
    # file_path - полный путь к файлу для загрузки
    # name - имя, под которым записать
    # storepath - путь, где записать
    # metadata - dict с метаданными
    key = Key(bucket)
    key.key = storepath + "/" + name

    key.set_metadata("user", amazon['AccessKey'])  # пользователь, закачавший файл
    for k, v in metadata.iteritems():
        print k + " - " + v
        key.set_metadata(k, v)
    
    key.set_contents_from_filename(file_path)

    return 0


def put_message_to_queue(data={}):
    m = Message()
    data['user'] = amazon['AccessKey']
    body = data.__str__()
    m.set_body(body)

    status = queue.write(m)
    if status:
        print "Message sent"
    else:
        print "ERROR sending message"
    return 0


def get_message_from_queue():
    rs = queue.get_messages()
    for m in rs:
        body = ast.literal_eval(m.get_body())
    return body


