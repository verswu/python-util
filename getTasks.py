import json

def deleteTasks():
	json_data = open('tasks.json').read()
	data = json.loads(json_data)

	taskIds = data['entries']

	for i in range(0,len(ids)):
		print ids[i]['id']

if __name__ == '__main__':
	deleteTasks()