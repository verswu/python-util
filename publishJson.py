import json
import urllib2
import sys

if len(sys.argv) == 2:
	token = sys.argv[1]
else:
	print "please provide token"
	sys.exit(0)

def find():
	json_data = open('tasks.json').read()
	data = json.loads(json_data)

	taskIds = data['entries']

	for i in range(0,len(taskIds)):
		url = taskIds[i]['contexts']['sourceMediaId'] + '?method=delete&token=' + token
		print url
	
if __name__ == '__main__':
	find()