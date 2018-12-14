#### Functions ##### 
# Without arguments, show help
# when the first argument is 'list', list reminders
# when the first argument is number, delete the record of the id number
# when 3 arguments are given, register new reminders

#### Issues #####
# show column when list reminders (not yet)
# do not write "DB connection" every time


import sqlite3
import os
import sys
from contextlib import closing
from datetime import datetime

args = sys.argv

### without any argument or too many arguments, just show help

if len(args) == 1 or len(args) > 4:
    print('list reminder : python ' + args[0] + ' list')
    print('add  reminder : python ' + args[0] + ' [due date] [pic] [task]')
    print('del  reminder : python ' + args[0] + ' [id]')

    sys.exit()

else:
    pass

ima = datetime.now().strftime("%Y-%m-%d %H:%M")
dbname = 'reminders.db'


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
    headers_on = '.headers on'
    mode_column = '.mode column'
    with closing(sqlite3.connect(dbname))as conn:
        c = conn.cursor()
        #c.execute(headers_on)
        #c.execute(mode_column)
        select_sql = 'select * from reminders'
        for row in c.execute(select_sql):
            print(row)

### function for insert ###

def insert_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        sql = 'insert into reminders (due_date, pic_name, task, register_date) values (?,?,?,?)'
        #reminder1 = (due_date, pic_name, task, ima)
        reminder1 = (args[1], args[2], args[3], ima)
        c.execute(sql, reminder1)
        conn.commit()

### function for delete ###

def delete_reminder():
    with closing(sqlite3.connect(dbname)) as conn:
        c = conn.cursor()
        sql = ''
        reminder1 = 


### if the first argument is 'list', show the list of reminder

if args[1] == 'list':
    list_reminder()

else:
    insert_reminder()


