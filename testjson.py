import json

json_data = open('test.json').read()
data = json.loads(json_data)

ids = data['entries']


for i in range(0,len(ids)):
	print ids[i]['mediaId']