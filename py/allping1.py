import sys
sys.path.append(r'libs') 
import IPy
from Ping import *
import threading
from Queue import Queue


def pinghost():		
		while not q.empty():	
				mutex.acquire(3)			
				host = q.get()
				print host
				mutex.release()
				conf1 = conf				
				conf1['host'] = host
				try:
						ping(conf1)
				except:
						print 1
				finally:
						q.task_done()


if __name__ == '__main__':
		conf = parseCmdOptions()
		hosts = conf['host']
		print hosts
		threads = []
		q = Queue()
		num_procs = 20
		hostlist=[]
		mutex = threading.Lock()
		ip = IPy.IP(hosts,make_net=True)
		for x in ip:
				hostlist.append(str(x))
		map(q.put,hostlist)
		for i in xrange(num_procs):
				c = threading.Thread(target=pinghost)
				c.setDaemon(True)
				threads.append(c)
		map(lambda x:x.start(),threads)
		q.join()








