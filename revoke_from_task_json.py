import json
import urllib2
import sys
import getToken

def publishTask():

	token = getToken.signIn()
	print token
	base = 'http://publish.po.ccp.cable.comcast.com/web/Publish/revoke?schema=1.2&token=' + token + '&account=http://access.auth.po.ccp.cable.comcast.com/data/Account/1025252577&form=json&_profileId=http://data.publish.po.ccp.cable.comcast.com/publish/data/PublishProfile/55007654&_mediaId='
	json_data = open('tasks_to_reset.json').read()
	data = json.loads(json_data)

	taskIds = data['entries']

	for i in range(0,len(taskIds)):
		url = base + taskIds[i]['contexts']['sourceMediaId'] 
		connection = urllib2.urlopen(url)
		response = connection.read()
		print str(i) + ' ' + response
		connection.close()		
	
if __name__ == '__main__':
	publishTask()

