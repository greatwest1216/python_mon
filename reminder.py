#### Basic Functions ##### 
# Without arguments, show help (done)
# when the first argument is 'list', list reminders (done)
# when the first argument is number, delete the record of the id number (done)
# when you delete the record, the verification message is given
# when 3 arguments are given, register a new reminder

#### Advanced Functions ##### 
# you can specify the due_date with 'kyo', 'asu', 'asatte', 'konshu', 'kongetsu' (not yet)

#### Issues #####
# show column when list reminders (not yet, low priority)
# do not write "connecting DB process" many times
# need improve for error handling such as 'python reminder.py hoge'

import sqlite3
import os
import sys
import re
import slackweb
from contextlib import closing
from datetime import datetime

args = sys.argv
ima = datetime.now().strftime("%Y-%m-%d %H:%M")
kyou = datetime.now().strftime("%Y-%m-%d")
dbname = 'reminders.db'
suuji = r'^[0-9]+$'
insert_message = 'New reminder is set.'
delete_message = 'The reminder is deleted.'
delete_cancel_message = 'Canceled.'

### without any argument or too many arguments, just show help

if len(args) == 1 or len(args) > 4:
    print('<Usage>')
    print('List reminders : python ' + args[0] + ' list')
    print('Add a reminder : python ' + args[0] + ' [due date] [pic] [task]')
    print('Del a reminder : python ' + args[0] + ' [id]')
    sys.exit()
else:
    pass

### Check if DB file exists 

if os.path.isfile(dbname):
    pass
else:
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        ## only for the first time ##
        create_table = '''create table if not exists reminders (id integer primary key autoincrement, due_date text, pic_name text, task text, register_date)'''
        c.execute(create_table)

### function for list ###

def list_reminder():
    headers_on = r'.headers on'
    mode_column = r'.mode column'
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
#        c.execute("headers on")
#        c.execute(mode_column)
        select_sql = 'select * from reminders'
        for row in c.execute(select_sql):
            print(row)

### function for insert ###

def insert_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        insert_sql = 'insert into reminders (due_date, pic_name, task, register_date) values (?,?,?,?)'
        record1 = (args[1], args[2], args[3], ima)
        c.execute(insert_sql, record1)
        conn.commit()
        print(insert_message)

### function for delete ###

def delete_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        delete_sql = 'delete from reminders where id = ?'
        record1 = (args[1]) 
        print("You're deleting reminder - id " + str(args[1]) + ".")
        kakunin = input("[Y/n]: ")
        if kakunin == 'Y':
            c.execute(delete_sql,record1)
            conn.commit()
            print(delete_message)
        else:
            print(delete_cancel_message)
    
### function for notify ###

def notify_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        select_sql1 = ''




### if the first argument is 'list', show the list of reminder

if args[1] == 'list':
    list_reminder()

elif re.match(suuji, args[1]):
    delete_reminder()

else:
    insert_reminder()


