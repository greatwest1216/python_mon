###################################
#  Script to monitor URL by http  #
###################################
import os
import sys
import requests
import slackweb
from lib import my_log_module as lg 

basedir = (os.path.dirname(os.path.abspath(__file__))).replace('\\','/')

### Slack webhook configuration ###

slackurl = basedir+'/files/slack_webhook_url.txt'
with open(slackurl) as urlfile:
    s = urlfile.read()
slack = slackweb.Slack(url=s)

### Logging Configuration ###

lg.logfile_name('URL')

### Create URL list from file ###

urllist = basedir+'/files/urllist.txt'
with open(urllist) as f:
    urls_tmp =  f.read().splitlines()
urls = [ s for s in urls_tmp if 'http' in s and '#' not in s ]

### Check the HTTP status code of each URL ###

for url in urls:
    res = requests.get(url, verify=False, headers={'Cache-Control': 'no-cache'})

    if res.status_code == 200:
        lg.logger.log(20, 'URL Check succeeded to ' + str(url))
    else:
        lg.logger.log(40, 'URL Check failed with [' + str(res.status_code) + '] to ' + str(url))
        slack.notify(text='URL Check failed with [' + str(res.status_code) + '] to ' + str(url))
