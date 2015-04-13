import revoke
import sys
min = 0
max = 0
if len(sys.argv) == 3:
		min = int(sys.argv[1])
		max = int(sys.argv[2])
		
def service_func():
	print 'Revoking...'

if __name__ == '__main__':
	service_func()
	for i in range(min,max+1):
		revoke.revoke(i,i+1)