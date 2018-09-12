#!/usr/bin/python
# -*- coding: utf-8 -*-
#*.py ip 1-1024 200
import sys
import socket
import threading
from Queue import Queue
def scan(host,port):
		s = socket.socket()
		s.settimeout(1)
		if s.connect_ex((host, port)) == 0:
				#print port, 'open'
				counting_open.append(port)
		s.close()
 
def worker(host):
		while not q.empty():
				mutex.acquire(3)
				port = q.get()
				mutex.release()
				try:
						scan(host,int(port))
				except:
						print 1
				finally:
						q.task_done()
 
if __name__ == '__main__':
		host = sys.argv[1]
		portlist = []
		mutex = threading.Lock()
		if sys.argv[2].find('-')>=0:
				portstrs = sys.argv[2].split('-')
				start_port = int(portstrs[0])
				end_port = int(portstrs[1])
				for port in range(start_port, end_port):
						portlist.append(port)
		elif sys.argv[2].find(',')>=0:
				portlist = sys.argv[2].split(',')
		else:
				portlist.append(sys.argv[2])
		counting_open = []
		q = Queue()
		threads = []
		num_procs = 500
		if len(sys.argv) ==4:
				num_procs = int(sys.argv[3])
		map(q.put,portlist)
		for i in xrange(num_procs):
				c = threading.Thread(target=worker,args=(host,))
				c.setDaemon(True)
				threads.append(c)
		map(lambda x:x.start(),threads)
		q.join()
		print host+" Opened ports:"
		print counting_open
