import json
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Optional
from nonebot import logger
from ..libs import Mcserver, User
from ..libs import server_list

sqdb: Optional[Connection] = None
cur: Optional[Cursor] = None


def init_sqlite():
    return sqlite3.connect("./data/sqlitedata.db")


def update_mcserver_info(mcserver: Mcserver):
    global cur
    if cur is None:
        cur = init_cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mcserver'")
    table_exists = cur.fetchall()
    if table_exists is None or len(table_exists) == 0:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS mcserver (
                server_ip TEXT,
                server_ping INTEGER,
                player_online INTEGER,
                player_max NUMERIC,
                player_list TEXT,
                server_version TEXT,
                server_motd TEXT,
                server_favicon TEXT,
                server_online INTEGER
            )
            ''')
    cur.execute("SELECT * FROM mcserver WHERE server_ip = ?", (mcserver.server_ip,))
    result = cur.fetchone()
    logger.info(result)
    if result is None:
        mcserver_dict = mcserver.dict()
        mcserver_dict["player_list"] = str(mcserver_dict["player_list"])
        logger.info(list(mcserver_dict.values()))
        cur.execute('''
            INSERT INTO mcserver (
                server_ip,
                server_ping,
                player_online,
                player_max,
                player_list,
                server_version,
                server_motd,
                server_favicon,
                server_online
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', list(mcserver_dict.values()))
    else:
        cur.execute('''
            UPDATE mcserver SET
                server_ping = ?,
                player_online = ?,
                player_max = ?,
                player_list = ?,
                server_version = ?,
                server_motd = ?,
                server_favicon = ?,
                server_online = ?
            WHERE server_ip = ?
            ''', (mcserver.server_ping,
                  mcserver.player_online,
                  mcserver.player_max,
                  str(mcserver.player_list),
                  mcserver.server_version,
                  mcserver.server_motd,
                  mcserver.server_favicon,
                  mcserver.server_ip,
                  mcserver.server_online,))
    sqdb_commit()


def get_mcserver_info(ip: str):
    global cur
    if cur is None:
        cur = init_cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='mcserver'")
    table_exists = cur.fetchall()
    if table_exists is None or len(table_exists) == 0:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS mcserver (
                server_ip TEXT,
                server_ping INTEGER,
                player_online INTEGER,
                player_max INTEGER,
                player_list TEXT,
                server_version TEXT,
                server_motd TEXT,
                server_favicon TEXT,
                server_online INTEGER
            )
            ''')
    cur.execute("SELECT * FROM mcserver WHERE server_ip = ?", (ip,))
    result = cur.fetchone()
    if result is None:
        server_state = Mcserver(
            server_ip=ip,
            server_online=0
        )
        return server_state
    else:
        server_state = Mcserver(
            server_ip=ip,
            server_ping=json.loads(result[1]),
            player_online=json.loads(result[2]),
            player_max=json.loads(result[3]),
            player_list=json.loads(result[4]),
            server_version=json.loads(result[5]),
            server_motd=json.loads(result[6]),
            server_favicon=json.loads(result[7]),
            server_online=json.loads(result[8]),
        )
        return server_state


def update_server_list(servers: server_list):
    global cur
    if cur is None:
        cur = init_cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='server_list'")
    table_exists = cur.fetchall()
    logger.info(table_exists)
    if table_exists is None or len(table_exists) == 0:
        cur.execute('''
                CREATE TABLE IF NOT EXISTS server_list (
                    mc_server TEXT,
                    mdt_server TEXT
                )
                ''')
    cur.execute("SELECT * FROM server_list WHERE rowid = 1")
    result = cur.fetchone()
    logger.info(result)
    if result is None:
        data_dict = servers.dict()
        data_json = {k: json.dumps(v) for k, v in data_dict.items()}
        logger.info(list(data_json.values()))
        cur.execute('''
        INSERT INTO server_list (
            mc_server,
            mdt_server
        ) VALUES (?, ?)
        ''', list(data_json.values()))
    else:
        db_data = server_list(
            mc_server_list=json.loads(result[0]),
            mdt_server_list=json.loads(result[1])
        )
        db_data_dict = db_data.dict()
        for k, v in servers.dict().items():
            db_data_dict[k] = list(set(db_data_dict[k] + v))
        db_data_json = {k: json.dumps(v) for k, v in db_data_dict.items()}
        cur.execute('''
        UPDATE server_list SET
            mc_server = ?,
            mdt_server = ?
        WHERE rowid = 1
        ''', list(db_data_json.values()))

    sqdb_commit()


def update_user_data(user: User):
    global cur
    if cur is None:
        cur = init_cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cur.fetchall()
    logger.info(user)
    if table_exists is None or len(table_exists) == 0:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                exp REAL,
                coins INTEGER,
                last_signin_date DATE
            )
        ''')

    cur.execute("SELECT * FROM users WHERE username = ?", (user.id,))
    existing_user = cur.fetchone()
    logger.info(existing_user)
    if existing_user is None:
        cur.execute('''
            INSERT INTO users (
                username,
                exp,
                coins,
                last_signin_date
            ) VALUES (?, ?, ?, ?)
        ''', (user.id, user.exp, user.coins, user.last_signin_date))
    else:
        cur.execute('''
            UPDATE users SET
                exp = ?,
                coins = ?,
                last_signin_date = ?
            WHERE username = ?
        ''', (user.exp, user.coins, user.last_signin_date, user.id))

    sqdb_commit()


def remove_server(server_ip: str):
    global cur
    if cur is None:
        cur = init_cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='server_list'")
    table_exists = cur.fetchall()
    logger.info(table_exists)
    if table_exists is None or len(table_exists) == 0:
        cur.execute('''
                CREATE TABLE IF NOT EXISTS server_list (
                    mc_server TEXT,
                    mdt_server TEXT
                )
                ''')
    cur.execute("SELECT * FROM server_list WHERE rowid = 1")
    result = cur.fetchone()
    logger.info(result)
    if result is None:
        return 0
    else:
        db_data = server_list(
            mc_server_list=json.loads(result[0]),
            mdt_server_list=json.loads(result[1])
        )
        db_data_dict = db_data.dict()
        remove_num: Optional[int] = 0
        for k, v in db_data_dict.items():
            if server_ip in v:
                v.remove(server_ip)
                remove_num += 1
                logger.info(v)
                db_data_dict[k] = v
        db_data_json = {k: json.dumps(v) for k, v in db_data_dict.items()}
        logger.info(db_data_json)
        cur.execute('''
                UPDATE server_list SET
                    mc_server = ?,
                    mdt_server = ?
                WHERE rowid = 1
                ''', list(db_data_json.values()))
    sqdb_commit()
    return remove_num


def get_user_data(user: User):
    global cur
    if cur is None:
        cur = init_cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cur.fetchall()

    if table_exists is None or len(table_exists) == 0:
        return None

    cur.execute("SELECT * FROM users WHERE username = ?", (user.id,))
    result = cur.fetchone()

    if result is None:
        return None
    else:
        user_data = User(
            id=result[0],
            exp=result[1],
            coins=result[2],
            last_signin_date=result[3]
        )
        return user_data


def get_server_list():
    global cur
    if cur is None:
        cur = init_cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='server_list'")
    table_exists = cur.fetchall()
    if table_exists is None or len(table_exists) == 0:
        return None

    cur.execute("SELECT * FROM server_list WHERE rowid = 1")
    result = cur.fetchone()
    if result is None:
        return None
    else:
        db_data = server_list(
            mc_server_list=json.loads(result[0]),
            mdt_server_list=json.loads(result[1])
        )
        return db_data


def init_cursor():
    global sqdb
    if sqdb is None:
        sqdb = init_sqlite()
    return sqdb.cursor()


def close_cursor():
    global sqdb, cur
    if sqdb is None:
        sqdb = init_sqlite()
    if cur is not None:
        cur.close()
    else:
        return None


def sqdb_commit():
    global sqdb
    if sqdb is None:
        sqdb = init_sqlite()
    sqdb.commit()


def close_sqdb():
    global sqdb
    if sqdb is None:
        sqdb = init_sqlite()
    sqdb.close()
