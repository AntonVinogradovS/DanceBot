import sqlite3 as sq
from create_bot import bot
import datetime

def sql_start():
    global base, cur
    base = sq.connect('data.db')
    cur = base.cursor()
    if base:
        print("Data base connected OK!")
    base.execute('CREATE TABLE IF NOT EXISTS wait(counter INTEGER PRIMARY KEY AUTOINCREMENT, checkPay TEXT, name TEXT, age TEXT, studio TEXT, phone TEXT,eMail TEXT, id TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS sweets(counter INTEGER PRIMARY KEY AUTOINCREMENT, checkPay TEXT, name TEXT, age TEXT, studio TEXT, phone TEXT,eMail TEXT, id TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS scheduled_mailing (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, launch_time TEXT)')
    base.commit()
async def sql_check_scheduled_mailing(user_id):
    cur.execute('SELECT user_id FROM scheduled_mailing WHERE user_id = ?', (user_id,))
    existing_user = cur.fetchone()
    return existing_user is not None

async def sql_add_scheduled_mailing(user_id):
    launch_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if not await sql_check_scheduled_mailing(user_id):
        cur.execute('INSERT INTO scheduled_mailing (user_id, launch_time) VALUES (?, ?)', (user_id, launch_time))
        base.commit()
    else:
        pass

async def sql_read_scheduled_mailing():
    cur.execute('SELECT user_id, launch_time FROM scheduled_mailing')
    rows = cur.fetchall()
    return rows

async def sql_remove_scheduled_mailing(user_id):
    cur.execute('DELETE FROM scheduled_mailing WHERE user_id = ?', (user_id,))
    base.commit()

async def sql_write(data, id):
    checkPay = data[5]
    name = data[0]
    age = data[1]
    studio = data[2]
    phone = data[3]
    eMail = data[4]
    cur.execute('INSERT INTO wait (checkPay, name, age, studio, phone, eMail, id) VALUES (?, ?, ?, ?, ?, ?, ?)', (checkPay, name, age, studio, phone, eMail, id))
    base.commit()

async def sql_read():
    cur.execute('SELECT * FROM wait')
    rows = cur.fetchall()
    return rows

async def sql_read_2():
    cur.execute('SELECT * FROM sweets')
    rows = cur.fetchall()
    return rows

async def sql_write_2(count):
    cur.execute('SELECT * FROM wait WHERE counter = ?', (count,))
    res = cur.fetchone()
    cur.execute('DELETE FROM wait WHERE counter = ?', (count,))
    cur.execute('INSERT INTO sweets (checkPay, name, age, studio, phone, eMail, id) VALUES (?, ?, ?, ?, ?, ?, ?)', (res[1], res[2], res[3], res[4], res[5], res[6], res[7]))
    base.commit()
