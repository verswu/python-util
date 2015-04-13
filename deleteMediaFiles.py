import json
import urllib2
import sys
import getToken

def deleteMediaFiles():
	token = getToken.signIn()
	account = 'http://access.auth.po.ccp.cable.comcast.com/data/Account/1122732678'
	json_data = open('delete_files.json').read()
	data = json.loads(json_data)
	ids = data['entries']
	f = open('media_ids.txt', 'wb')
	print 'Deleting MediaFiles...'

#"mediaId": "http://data.media.po.ccp.cable.comcast.com/media/data/Media/158843100"

	for i in range(0,len(ids)):
		url = 'http://fms.po.ccp.cable.comcast.com/web/FileManagement/deleteFile?schema=1.5&form=json&token=' + token + '&account=' + account + '&_fileId=' + ids[i]['id']

		print str(i) + ' ' + url
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

		    f.write(ids[i]['mediaId'] + '\n' )
	

if __name__ == '__main__':
	deleteMediaFiles()
