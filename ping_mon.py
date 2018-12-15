# When ping fails, popup shows up (done)
# If this laptop is not connected to DSF LAN, monitoring should be temporarily stopped (done)
# Create one file per day for logging (done)
# cron this script every 10 minutes (done)
# you can use fqdn instead of IP address
# you can comment out host by '#' (done)
# when failure popup should show up (*** with task scheduler, it does not work)
# ping can be conducted in parallel for many hosts

import pings
import logging, datetime
import sys
#from win10toast import ToastNotifier

### Logging Configuration ###

# log file name
today1 = datetime.date.today()
logfile1 = 'logs/'+str(today1)+'.log'
# Initiate logger
logger = logging.getLogger('LoggingTest')
# Logger level
logger.setLevel(10)
# Log file
fh = logging.FileHandler(logfile1)
logger.addHandler(fh)
# Log Format
formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
fh.setFormatter(formatter)

### Check if in LAN ###

p = pings.Ping()
res = p.ping('10.1.20.254', times=3)

if not res.is_reached():
    logger.log(10, "Laptop is not connected to LAN")
    sys.exit()
else:
    pass

### Create host list from file ###

with open(r'D:\monitoring\hostlist', "r") as f:
    hosts_tmp = f.read().splitlines()
# exclude items who do not include '.' or who includes '#'
hosts = [s for s in hosts_tmp if '.' in s and '#' not in s]

### Ping each host to monitor and log it ###

p = pings.Ping()

for host in hosts:
    res = p.ping(host, times=3)

    if res.is_reached():
        logger.log(20, "Ping succeeded to "+str(host))
    else:
        logger.log(20, "Ping FAILED to "+str(host))
#        toaster = ToastNotifier()
#        toaster.show_toast(title='Ping Failed', msg=str(host), duration=5, threaded=True)

