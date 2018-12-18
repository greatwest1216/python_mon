#### Basic Functions ##### 
# Without arguments, show help (done)
# when the first argument is 'list', list reminders (done)
# when the first argument is number, delete the record of the id number (done)
# when you delete the record, the verification message is given (done)
# when 3 arguments are given, register a new reminder (done)
# the third argument for 'task' can include blank (done)
# when the reminder is done, don't delete the record itself but just hide from SELECT results by adding new column

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
dbname = 'files/reminders.db'
suuji = r'^[0-9]+$'
nengappi = r'20[0-9]{2}-[0-9]{2}-[0-9]{2}'
nichiji = r'[0-9]{2}-[0-9]{2}'
insert_message = 'New reminder is set.'
delete_message = 'The reminder is deleted.'
delete_cancel_message = 'Canceled.'
slackurl = 'files/slack_webhook_url.txt'
with open(slackurl) as urlfile:
    s = urlfile.read()
slack = slackweb.Slack(url=s)

### without any argument or too many arguments, just show help
### if args[3] includes blank, it is merged into one argument

if len(args) == 1:
    print('<Usage>')
    print('List reminders : python ' + args[0] + ' list.')
    print('Add a reminder : python ' + args[0] + ' [due date] [pic] [task].')
    print('Del a reminder : python ' + args[0] + ' [id].')
    sys.exit()
elif len(args) >= 5:
    i = 4
    while i <= len(args) - 1:
        args[3] = args[3] + " " + args[i]
        i = i + 1
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
        create_table = '''CREATE TABLE IF NOT EXISTS reminders (id integer primary key autoincrement, status text default 'OPEN', due_date text, pic_name text, task text, register_date)'''
        c.execute(create_table)

### Function for list ###

def list_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql = 'SELECT SUBSTR("00"||id,-2,2) AS id, due_date, SUBSTR(pic_name||"               ",1,10) AS pic_name, task FROM reminders WHERE status = "OPEN"'
        for row in c.execute(select_sql):
            print(row)

### Function for insert ###

def insert_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        insert_sql = 'INSERT INTO reminders (due_date, pic_name, task, register_date) VALUES (?,?,?,?)'
        record = (args[1], args[2], args[3], ima)
        c.execute(insert_sql, record)
        conn.commit()
        print(insert_message)

### Function for delete ###

def delete_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()

        # check if the id's record exists (not yet)

        #delete_sql = 'DELETE FROM reminders WHERE id = ?'
        update_sql = 'UPDATE reminders SET status = "DONE" WHERE id = ?'
        record = (args[1],) 
        print("You're deleting reminder - id " + str(args[1]) + ".")
        kakunin = input("[Y/n]: ")
        if kakunin == 'Y':
            c.execute(update_sql, record)
            conn.commit()
            print(delete_message)
        else:
            print(delete_cancel_message)
    
### Function for notify ###

def notify_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        #select_sql1 = "SELECT pic_name || '     ' || task FROM reminders WHERE due_date = ?"
        select_sql1 = 'SELECT SUBSTR("000"||id,-3,3) || "  " || SUBSTR(pic_name||"               ",1,10) || "  " || task FROM reminders WHERE due_date = ? and status = "OPEN"'
        record1 = (kyou,)
        reminders_kyou = ''
        for row in c.execute(select_sql1, record1):
            reminders_kyou = reminders_kyou + str(row).split("'")[1] + '\n'
#            print(row)
        slacktext = '''Today's reminders are below:

id  who         task
''' + reminders_kyou + '''
'''
        print(slacktext)        
        slack.notify(text=slacktext)

### Run each Function based of the args[1]

if args[1] == 'list':
    list_reminder()

elif args[1] == 'notify':
    notify_reminder()

elif re.match(suuji, args[1]):
    delete_reminder()

else:
    insert_reminder()


