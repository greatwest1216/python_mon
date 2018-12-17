#### Basic Functions ##### 
# Without arguments, show help (done)
# when the first argument is 'list', list reminders (done)
# when the first argument is number, delete the record of the id number (done)
# when you delete the record, the verification message is given
# when 3 arguments are given, register a new reminder
# the third argument for 'task' can include blank

#### Advanced Functions ##### 
# you can specify the due_date with 'kyo', 'asu', 'asatte', 'konshu', 'kongetsu' (not yet)
# you can skip mentioning YYYY (need processing args[1]) (done)
# encrypt database file
# specify the number of letters in the column (done)

#### Issues #####
# show column when list reminders (done)
# do not write "connecting DB process" many times
# need improve for error handling such as 'python reminder.py hoge'
# modify the SQL (select -> SELECT) etc (done)

import sqlite3
import os
import sys
import re
import slackweb
from contextlib import closing
from datetime import datetime
from datetime import timedelta
#from dateutil import relativedelta
# pip install python-dateutil

args = sys.argv
now = datetime.now()
ima = datetime.now().strftime("%Y-%m-%d %H:%M")
kyou = datetime.now().strftime("%Y-%m-%d")
nen = datetime.now().strftime("%Y")
ashita = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
asatte = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")
shiasatte = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
#konshu
#kongetsu
#monday getsuyou
#tuesday kayou
#...
dbname = 'reminders.db'
suuji = r'^[0-9]+$'
nengappi = r'20[0-9]{2}-[0-9]{2}-[0-9]{2}'
nichiji = r'[0-9]{2}-[0-9]{2}'
insert_message = 'New reminder is set.'
delete_message = 'The reminder is deleted.'
delete_cancel_message = 'Canceled.'
slackurl = 'D:/monitoring/slack_webhook_url.txt'
with open(slackurl) as urlfile:
    s = urlfile.read()
slack = slackweb.Slack(url=s)

### without any argument or too many arguments, just show help

if len(args) == 1 or len(args) > 4:
    print('<Usage>')
    print('List reminders : python ' + args[0] + ' list')
    print('Add a reminder : python ' + args[0] + ' [due date] [pic] [task]')
    print('Del a reminder : python ' + args[0] + ' [id]')
    sys.exit()
else:
    pass

### Process args[1] if needed

if re.match(nengappi, args[1]):
    pass
elif re.match(nichiji, args[1]):
    args[1] = nen + "-" + args[1]
elif args[1] == 'kyou':
    args[1] = kyou
elif args[1] == 'ashita':
    args[1] = ashita
elif args[1] == 'asatte':
    args[1] = asatte
elif args[1] == 'shiasatte':
    args[1] = shiasatte
else:
    pass



### Check if DB file exists 

if os.path.isfile(dbname):
    pass
else:
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        ## only for the first time ##
        create_table = '''CREATE TABLE IF NOT EXISTS reminders (id integer primary key autoincrement, due_date text, pic_name text, task text, register_date)'''
        c.execute(create_table)

### function for list ###

def list_reminder():
    headers_on = r'.headers on'
    mode_column = r'.mode column'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
#        c.execute("headers on")
#        c.execute(mode_column)
        #select_sql = 'SELECT * FROM reminders'
        select_sql = 'SELECT substr("00"||id,-2,2) as id, due_date, substr(pic_name||"               ",1,10) as pic_name, task FROM reminders'
        for row in c.execute(select_sql):
            print(row)

### function for insert ###

def insert_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        insert_sql = 'INSERT INTO reminders (due_date, pic_name, task, register_date) VALUES (?,?,?,?)'
        record = (args[1], args[2], args[3], ima)
        c.execute(insert_sql, record)
        conn.commit()
        print(insert_message)

### function for delete ###

def delete_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        # check if the id's record exists (not yet)

        delete_sql = 'DELETE FROM reminders WHERE id = ?'
        record = (args[1],) 
        print("You're deleting reminder - id " + str(args[1]) + ".")
        kakunin = input("[Y/n]: ")
        if kakunin == 'Y':
            c.execute(delete_sql, record)
            conn.commit()
            print(delete_message)
        else:
            print(delete_cancel_message)
    
### function for notify ###

def notify_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        #select_sql1 = "SELECT pic_name || '     ' || task FROM reminders WHERE due_date = ?"
        select_sql1 = 'SELECT substr("00"||id,-2,2) || "  " || substr(pic_name||"               ",1,10) || "  " || task FROM reminders WHERE due_date = ?'
        record1 = (kyou,)
        reminders_kyou = ' '
        for row in c.execute(select_sql1, record1):
            reminders_kyou = reminders_kyou + str(row).split("'")[1] + '\n '
#            print(row)
        slacktext = '''Today's reminders are below:
 id  who               task
''' + reminders_kyou + '''
'''
        print(slacktext)        
        slack.notify(text=slacktext)

### if the first argument is 'list', show the list of reminder

if args[1] == 'list':
    list_reminder()

elif args[1] == 'notify':
    notify_reminder()

elif re.match(suuji, args[1]):
    delete_reminder()

else:
    insert_reminder()


