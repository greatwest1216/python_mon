# you can use fqdn instead of IP address (not yet)
# ping can be conducted in parallel for many hosts (if possible)

import pings
import logging, datetime
import sys
import slackweb
from lib import my_log_module as lg

### Slack webhook configuration ###
slackurl = 'files/slack_webhook_url.txt'
with open(slackurl) as urlfile:
    s = urlfile.read()
slack = slackweb.Slack(url=s)

### Logging Configuration ###

lg.logfile_name('ping')

### Check if in LAN ###

p = pings.Ping()
res = p.ping('10.1.20.254', times=3)

if not res.is_reached():
    lg.logger.log(10, "Laptop is not connected to LAN")
    sys.exit()
else:
    pass

### Create host list from file ###

hostlist = 'files/hostlist.txt'
with open(hostlist) as f:
    hosts_tmp = f.read().splitlines()
# exclude items who do not include '.' or who includes '#'
hosts = [s for s in hosts_tmp if '.' in s and '#' not in s]

### Ping each host to monitor and log it ###

p = pings.Ping()

for host in hosts:
    res = p.ping(host, times=3)

    if res.is_reached():
        lg.logger.log(20, "Ping succeeded to "+str(host))
    else:
        lg.logger.log(20, "Ping FAILED to "+str(host))
        slack.notify(text="Ping failed to "+str(host)+".")

