#!/usr/bin/python

import sys, serial, time, datetime, json, pymongo

with open('estufas.cfg', 'r') as filecfg:
	config = json.load(filecfg)
filecfg.close()

try:
	conn=pymongo.MongoClient(config['dbhostname'],config['dbhostport'])
except pymongo.errors.ConnectionFailure, e:
	print "Could not connect to MongoDB: %s" % e 

db = conn[config['dbname']]
collection = db['estufa_teste']

try:
	ser = serial.Serial(config['serialport'], 9600)
	time.sleep(5)
	ser.flushInput()
	while True:
		lst = []
		for i in range(1, 100):
			doc = {} 
			vlrSensor = ser.readline()
			items = vlrSensor.translate(None, '\r\n').split(' , ')
			for i in items:	
				doc[i.split(' : ')[0]] = i.split(' : ')[1] 
			doc['dataehora'] = datetime.datetime.now()
			lst.append(doc.copy())
			print doc
		collection.insert_many(lst)		
except KeyboardInterrupt:
	pass
finally:
	ser.close()
