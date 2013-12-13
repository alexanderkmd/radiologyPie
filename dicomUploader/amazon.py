#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from boto.s3.connection import S3Connection
import config

amazon = config.get_config_section("Amazon")
s3conn = S3Connection(amazon['AccessKey'], amazon['SecretKey'])

bucket = s3conn.get_bucket(amazon['bucket'])

for item in bucket.list():
    print item.name