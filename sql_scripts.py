import sqlite3
from config import *


def admin_users():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("SELECT admin FROM admin_table")
    admins = cursor.fetchall()
    admins = [i[0] for i in admins]

    return admins


def add_user_to_db(user_id, username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO user (user_id, username, rights, date_end_sub, active_task) VALUES(?, ?, ?, ?, ?)", (user_id, username, 0, None, 0,))

    conn.commit()
    conn.close()


def check_user_exists(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id,))
    user = bool(len(result.fetchall()))

    conn.close()

    return user


def user_id_by_username(username):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user WHERE username = ?", (username,))
    user = result.fetchone()[0]

    conn.close()

    return user


def change_users_rights(username, rights, new_date):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET rights = ?, date_end_sub = ? WHERE username = ?", (rights, new_date, username,))

    conn.commit()
    conn.close()


def check_users_rights(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT rights FROM user WHERE user_id = ?", (user_id,))
    rights = result.fetchone()[0]

    conn.close()

    return rights


def get_list_of_users_with_rights():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT user_id FROM user WHERE rights = ?", (1,))
    users = result.fetchall()
    users = [i[0] for i in users if i != None]

    conn.close()

    return users


def users_end_sub_date(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT date_end_sub FROM user WHERE user_id = ?", (user_id,))
    end_sub_date = result.fetchone()[0]

    conn.close()

    return end_sub_date


def auto_demote_users(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET rights = ?, date_end_sub = ? WHERE user_id = ?", (0, None, user_id,))

    conn.commit()
    conn.close()


def get_active_task_status(user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT active_task FROM user WHERE user_id = ?", (user_id,))
    active_task_status = result.fetchone()[0]

    conn.close()

    return active_task_status


def change_active_task_status(status, user_id):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("UPDATE user SET active_task = ? WHERE user_id = ?", (status, user_id,))

    conn.commit()
    conn.close()


def get_hash_list():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    result = cursor.execute("SELECT txs_hash FROM hash_list")
    txs_hash = result.fetchall()
    txs_hash_list = [i[0] for i in txs_hash if i != None]

    conn.close()

    return txs_hash_list


def txs_hash_append_in_bd(txs_hash):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    cursor.execute("INSERT INTO hash_list (txs_hash) VALUES(?)", (txs_hash,))

    conn.commit()
    conn.close()
