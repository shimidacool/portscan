import sys
sys.path.append(r'libs') 
import IPy
from Ping import *

conf = parseCmdOptions()
hosts = conf['host']
print hosts
ip = IPy.IP(hosts,make_net=True)
for x in ip:
    conf['host'] = str(x)
    ping(conf)



