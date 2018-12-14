#### Functions ##### 
# when the first argument is 'list', list reminders
# when the first argument is number, delete the record of the id number
# when 3 arguments are given, register new reminders

#### Issues #####
# show column when list reminders (not yet)
# do not write "DB connection" every time


import sqlite3
import sys
from contextlib import closing
from datetime import datetime

args = sys.argv
ima = datetime.now().strftime("%Y-%m-%d %H:%M")
dbname = 'reminders.db'


### Anyway connect DB first (define c as the global variables) ###

with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()
    ## only for the first time ##
    create_table = '''create table if not exists reminders (id integer primary key autoincrement, due_date text, name text, task text, register_date)'''
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
    
    

list_reminder()

sys.exit()

### function for insert ###



with closing(sqlite3.connect(dbname)) as conn:
    c = conn.cursor()
    ## only for the first time ##
    create_table = '''create table if not exists reminders (id integer primary key autoincrement, due_date text, name text, task text, register_date)'''
    c.execute(create_table)

    list_reminder()
    sys.exit()



    sql = 'insert into reminders (due_date, name, task, register_date) values (?,?,?,?)'
    reminder1 = ('2018-12-31', 'osajima', 'WAAS contract', ima)
    c.execute(sql, reminder1)

    conn.commit()

