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

# return list of Media IDs that has the determined category
def getMediaByCategory():
	#Set the category to search for and account here:
	account= 'Comcast%20PAR%20Syndication%20Production%20-%20Main'
	category = "cox"
	mediaURL = config.get('synd_services', 'media')
	query = mediaURL + 'data/Media?schema=1.7.0&searchSchema=1.0&form=cjson&pretty=true&byCategories=' + category + '&account=' + account + '&token=' + token	
	
	#get count:
	countQuery = query + '&count=true&entries=false'
	print countQuery
	connection = urllib2.urlopen(countQuery)
	data = None
	try:
		data = json.loads(connection.read())
	except urllib2.URLError:
		print 'Oops! Timeout Error! Sorry!'
	connection.close()
	count = data['totalResults']
	print 'There are ' + str(count) + ' assets with a category of ' + category

	#build initial list of MediaIDs
	print 'Building list of MediaIDs'
	assets =[]
	i = 0
	while i <= count:
	#while i <= 10050:	
		getQuery = query + '&fields=id&range=' + str(i) + '-' + str(i+1000)
		connection = None
		try:
			connection = urllib2.urlopen(getQuery)
		except urllib2.URLError:
			print 'Oops! Timeout Error! Sorry!'
		data = json.loads(connection.read())
		connection.close()
		entries = data['entries']
		for x in range(0,len(entries)):
			id = entries[x]['id']
			assets.append(id)
		i += 1000

	return assets

def getMediaByProvider():
	#Set the provider to search for and account here:
	account= 'Comcast%20PAR%20Syndication%20Production%20-%20Main'
	provider = "cox"
	mediaURL = config.get('synd_services', 'media')
	query = mediaURL + 'data/Media?schema=1.7.0&searchSchema=1.0&form=cjson&pretty=true&byProvider=' + provider + '&account=' + account + '&token=' + token	
	
	#get count:
	countQuery = query + '&count=true&entries=false'
	print countQuery
	connection = None
	try:
		connection = urllib2.urlopen(countQuery)
	except urllib2.URLError:
		print 'Oops! Timeout Error! Sorry!'
	data = json.loads(connection.read())
	connection.close()
	count = data['totalResults']
	print 'There are ' + str(count) + ' assets with a provider of ' + provider

	#build initial list of MediaIDs
	print 'Building list of MediaIDs'
	assets =[]
	i = 0
	while i <= count:
	#while i <= 10050:	
		getQuery = query + '&fields=id&range=' + str(i) + '-' + str(i+1000)
		connection = None
		try:
			connection = urllib2.urlopen(getQuery)
		except urllib2.URLError:
			print 'Oops! Timeout Error! Sorry!'
		data = json.loads(connection.read())
		connection.close()
		entries = data['entries']
		for x in range(0,len(entries)):
			id = entries[x]['id']
			assets.append(id)
		i += 1000

	return assets

def repairAssets(mergedList):

	workflowURL = config.get('synd_services', 'workflow')
	publishProfile = 'http://data.publish.theplatform.com/publish/data/PublishProfile/18526937'
	shareProfile = 'http://data.share.theplatform.com/sharing/data/OutletProfile/19026'
	f = open('media_ids_to_share.txt', 'wb')

	workflowQuery = workflowURL + 'data/ProfileResult?schema=1.3.0&form=cjson&pretty=true&fields=status&token=' + token + '&byProfileId='
	#repair media in the list 1 by 1
	for media in mergedList:
		publishQuery = workflowQuery + publishProfile + '&byMediaId=' + media
		publishStatus = checkStatus(publishQuery)
		#DEBUG print media
		#DEBUG print '		-Workflow Selector status: ' + publishStatus
		#If published to Workflow Selector, check if it is shared to COX

		if publishStatus == "Processed":
			shareQuery = workflowQuery + shareProfile + '&byMediaId=' + media
			shareStatus = checkStatus(shareQuery)
			#DEBUG print '		-CoxRefShare status: ' + shareStatus
			if shareStatus != "Processed":
				print media
				f.write(media + '\n' )
				f.flush()

def checkStatus(query):
	connection = None
	try:
		connection = urllib2.urlopen(query)
	except urllib2.URLError:
		print 'Timeout Error checking media '
	data = json.loads(connection.read())
	connection.close()
	entries = data['entries']
	if len(entries) > 0:
		if entries[0]['status'] == "Processed":
			return "Processed"
		else: 
			return entries[0]['status']	
	return 'Not Published'

if __name__ == '__main__':
	config = ConfigParser.ConfigParser()
	config.readfp(open(r'config.properties'))
	token = getToken()
	cox_category_assets = getMediaByCategory()
	cox_provider_assets = getMediaByProvider()
	mergedList = set(cox_provider_assets + cox_category_assets)
	repairAssets(mergedList)
