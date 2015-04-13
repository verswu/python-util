import json
import urllib2
import sys
import getToken

def resetTasks():
	token = getToken.signIn()
	print token
	json_data = open('tasks_to_reset.json').read()
	data = json.loads(json_data)

	taskIds = data['entries']

	for i in range(0,len(taskIds)):
		url = 'http://fms.po.ccp.cable.comcast.com/web/FileManagement/resetTask?schema=1.4&token=' + token + '&form=json&_taskId='
		url += taskIds[i]['id']
		connection = urllib2.urlopen(url)
		response = connection.read()
		print str(i) + ' ' + response
		connection.close()		

if __name__ == '__main__':
	resetTasks()
