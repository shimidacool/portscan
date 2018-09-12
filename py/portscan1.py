#!/usr/bin/python
# -*- coding: utf-8 -*-
#*.py ip 1-1024 200
import sys
sys.path.append(r'libs') 
import socket
from multiprocessing import Pool

def scan(host,port):
		s = socket.socket()
		s.settimeout(1)
		if s.connect_ex((host, port)) == 0:
				print port, 'open'
		s.close()

def run(args):
    scan(args[0], args[1])


if __name__ == '__main__':
		host = sys.argv[1]
		portlist = []
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
		num_procs = 500
		if len(sys.argv) ==4:
				num_procs = int(sys.argv[3])
		pool = Pool(processes=num_procs)
		paras = [(host, int(port)) for port in portlist]
		pool.map(run, paras)
