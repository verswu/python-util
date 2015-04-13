import urllib2
import re
import sys
import json

min = 0
max = 0
if len(sys.argv) == 4:
		min = int(sys.argv[1])
		max = int(sys.argv[2])
		token = sys.argv[3]

def publish(min, max, token):

	base = 'http://publish.po.ccp.cable.comcast.com/web/Publish/publish?schema=1.2&token=' + token + '&account=http://access.auth.po.ccp.cable.comcast.com/data/Account/1091840537&form=json&_profileId=http://data.publish.po.ccp.cable.comcast.com/publish/data/PublishProfile/60137121&_mediaId='

	json_data = open('cmp.json').read()
	data = json.loads(json_data)

	ids = data['entries']


	for i in range(0,len(ids)):
		url = base + ids[i]['mediaId']
		try: 
			connection = urllib2.urlopen(url)
		except urllib2.HTTPError, e:
			checksLogger.error('HTTPError = ' + str(e.code))
		except urllib2.URLError, e:
			checksLogger.error('URLError = ' + str(e.reason))
		except httplib.HTTPException, e:
			checksLogger.error('HTTPException')
		except Exception:
			import traceback
			checksLogger.error('generic exception: ' + traceback.format_exc())
		
		
		response = connection.read()
		print str(i) + ' ' + response
		connection.close()

if __name__ == '__main__':
	publish(min, max, token)