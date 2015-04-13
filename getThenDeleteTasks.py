import json
import urllib2
import sys
import ConfigParser

# return token
def getToken():
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'config.properties'))

	identityURL = config.get('services', 'identity')	
	username = config.get('credentials', 'username')
	password = config.get('credentials', 'password')
	url = identityURL + 'web/Authentication/signIn?schema=1.0&form=json&username=' + username + '&password=' + password
	
	print 'Signing in...'
	connection = urllib2.urlopen(url)
	response = connection.read()
	d = json.loads(response)
	connection.close()
	return d['signInResponse']['token']

#get and return tasks in ads account that fulfill the following
#  1. status = inProgress or inProgressWithErrors
#  2. taskType = Move
def getTasks():
	url = 'http://data.task.po.ccp.cable.comcast.com/task/data/Task?schema=1.3.0&form=cjson&pretty=true&fields=id,status,taskType,attemptNumber&byStatus=inProgressWithErrors%7CinProgress%7Cfailed&byTaskType=thePlatform.RMP.Task.Move&count=true&token=' + token + '&account=vms%20poc%20advertising%20ingest'
	connection = urllib2.urlopen(url)
	data = json.loads(connection.read())
	return data	
	connection.close()

#deletes the task if it is on any attempt except the first one
def deleteTasks(data):
	taskIds = data['entries']
	print 'Checking ' + str(len(taskIds)) + ' current Move tasks...'
	for i in range(0,len(taskIds)):
		attemptNumber = taskIds[i]['attemptNumber']
		id = taskIds[i]['id']
		if attemptNumber > 2:
			url = id + '?method=delete&token=' + token
			connection = urllib2.urlopen(url)
			response = connection.read()
			print 'delete number ' + str(i) + '- ' + response
			connection.close()
		else: 
			print 'On try #' + str(attemptNumber) + ', not deleting ' + id	

if __name__ == '__main__':
	token = getToken()
	data = getTasks()
	deleteTasks(data)
