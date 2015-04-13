import json
import urllib2
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(open(r'config.properties'))

def signIn():
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
	

if __name__ == '__main__':
	signIn()