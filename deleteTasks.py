import json
import urllib2
import sys
import getToken

def deleteTasks():
	token = getToken.signIn()
	print token
	json_data = open('first_pass.json').read()
	data = json.loads(json_data)

	taskIds = data['entries']
	f = open('broken1.txt', 'wb')


	for i in range(0,len(taskIds)):
		url = taskIds[i]['id'] + '?method=delete&token=' + token
		print url
		try:
			connection = urllib2.urlopen(url)
			response = connection.read()
			print str(i) + ' ' + response
		except urllib2.HTTPError, err:
		    if err.code == 404:
		        print "Page not found!"
		    elif err.code == 403:
		        print "Access denied!"
		    elif err.code == 500:
		        print "Access denied!"
		    else:
		        print "Something happened! Error code", err.code
		    f.write(taskIds[i]['id'] + '\n' )
	

if __name__ == '__main__':
	deleteTasks()
