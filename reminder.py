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
raishu = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
#kongetsu
#monday getsuyou
#tuesday kayou
#...
basedir = (os.path.dirname(os.path.abspath(__file__))).replace('\\','/')
dbname = basedir+'/files/reminders.db'
suuji = r'^[0-9]+$'
nengappi = r'20[0-9]{2}-[0-9]{2}-[0-9]{2}'
nichiji = r'[0-9]{2}-[0-9]{2}'
insert_message = 'New reminder is set.'
delete_message = 'The reminder is deleted.'
update_message =  'The reminder is updated.'
cancel_message = 'Canceled.'
slackurl = basedir+'/files/slack_webhook_url.txt'
with open(slackurl) as urlfile:
    s = urlfile.read()
slack = slackweb.Slack(url=s)

### without any argument or too many arguments, just show help
### if args[3] includes blank, it is merged into one argument

if len(args) == 1:
    print('<Usage>')
    print('List reminders    : python /path/to/reminder.py list.')
    print('Add new reminder  : python /path/to/reminder.py [due date] [pic] [task].')
    print('Update a reminder : python /path/to/reminder.py [id].')
    sys.exit()
elif len(args) >= 5:
    i = 4
    while i <= len(args) - 1:
        args[3] = args[3] + " " + args[i]
        i = i + 1
else:
    pass

def process_date(x):
    if re.match(nengappi, x):
        return x
    elif re.match(nichiji, x):
        x = nen + "-" + x
        return x
    elif x == 'kyou':
        x = kyou
        return x
    elif x == 'ashita':
        x = ashita
        return x
    elif x == 'asatte':
        x = asatte
        return x
    elif x == 'shiasatte':
        x = shiasatte
        return x
    elif x == 'raishu':
        x = raishu
        return x
    else:
        return x

if args[1] != process_date(args[1]):
    due_date0 = process_date(args[1]) 
else: 
    id0 = args[1]

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
        #select_sql = 'SELECT SUBSTR("00"||id,-2,2) AS id, due_date, SUBSTR(pic_name||"               ",1,10) AS pic_name, task FROM reminders WHERE status = "OPEN" AND date(due_date) <= date("now", "+14 days") ORDER BY due_date'
        select_sql = 'SELECT SUBSTR("000"||id,-3,3) || "  " || due_date || "  " || SUBSTR(pic_name||"               ",1,10) || "  " || task FROM reminders WHERE status = "OPEN" AND date(due_date) <= date("now", "+14 days") ORDER BY due_date'
        for row in c.execute(select_sql):
            print(row)

### Function for insert ###

def insert_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        insert_sql = 'INSERT INTO reminders (due_date, pic_name, task, register_date) VALUES (?,?,?,?)'
        record = (due_date0, args[2], args[3], ima)
        c.execute(insert_sql, record)
        conn.commit()
        print(insert_message)

### Function for delete ###

def update_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        # check if the id's record exists (not yet)
        select_sql1 = 'SELECT due_date, pic_name, task FROM reminders WHERE id = ?'
        delete_sql1 = 'UPDATE reminders SET status = "DONE" WHERE id = ?'
        record1 = (id0,) 
        for row in c.execute(select_sql1, record1):
            due_date1 = row[0]
            pic_name1 = row[1]
            task1 = row[2]
        print("You're updating this reminder - %s %s %s" % (due_date1, pic_name1, task1))
        kakunin = input("[Done/Update/n]: ")
        if kakunin.lower() == 'd':
            c.execute(delete_sql1, record1)
            conn.commit()
            print(delete_message)
        elif kakunin.lower() == 'u':

            input_due_date = input("[%s]: " % (due_date1)) 
            if input_due_date == '':
                pass
            else:
                input_due_date = process_date(input_due_date)
                update_sql1 = 'UPDATE reminders SET due_date = ? WHERE id = ?'
                record2 = (input_due_date, id0)
                c.execute(update_sql1, record2)
                conn.commit()
                print(update_message)

            input_pic_name = input("[%s]: " % (pic_name1)) 
            if input_pic_name == '':
                pass
            else:
                update_sql2 = 'UPDATE reminders SET pic_name = ? WHERE id = ?'
                record3 = (input_pic_name, id0)
                c.execute(update_sql2, record3)
                conn.commit()
                print(update_message)

            input_task = input("[%s]: " % (task1)) 
            if input_task == '':
                pass
            else:
                update_sql3 = 'UPDATE reminders SET task = ? WHERE id = ?'
                record4 = (input_pic_name, id0)
                c.execute(update_sql3, record4)
                conn.commit()
                print(update_message)

        else:
            print(cancel_message)
    
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
    update_reminder()
else:
    insert_reminder()


