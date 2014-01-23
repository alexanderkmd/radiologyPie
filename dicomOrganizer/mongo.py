#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import datetime
import pymongo
from pymongo import MongoClient

mongo_url="mongodb://user:password@dharma.mongohq.com:10048/db"

client = MongoClient(mongo_url)

db = client.probadb

print db.collection_names()

collection = db.images

count = collection.count()
print "Images in DB: ", count

image = {"name": "хренатень", "where": "CWG", "dateAdded": datetime.datetime.utcnow() }

imageid = collection.insert(image)

print imageid