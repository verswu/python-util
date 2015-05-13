import json
import urllib2
import sys
import ConfigParser

# return token
def getToken():
	identityURL = config.get('synd_services', 'identity')
	username = config.get('credentials', 'synd_username')
	password = config.get('credentials', 'synd_password')
	url = identityURL + 'web/Authentication/signIn?schema=1.0&form=json&username=' + username + '&password=' + password
	
	print 'Signing in...'
	connection = urllib2.urlopen(url)
	response = connection.read()
	d = json.loads(response)
	connection.close()
	return d['signInResponse']['token']

def publishFromList():
	fname = 'media_ids_to_share.txt'
	content = None
	sharingBase = config.get('synd_services', 'sharing')
	sharingProfile = 'http://data.share.theplatform.com/sharing/data/OutletProfile/19026'
	sharingURL = sharingBase + '?schema=1.1&form=json&token=' + token + '&account=http://access.auth.theplatform.com/data/Account/2657272111&form=json&_profileId=' + sharingProfile + '&_mediaId='   

	with open(fname) as f:
		content = f.readlines()
	for media in content:
		query = sharingURL + media
		print query
		publish(query)

def publish(query):
	try:
		connection = urllib2.urlopen(query)
		data = json.loads(connection.read())
		connection.close()
		if data['isException'] == True:
			print 'FAILURE: '
			print data

	except urllib2.URLError:
		print 'Timeout Error sharing media '



if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'config.properties'))
	token = getToken()
	publishFromList()