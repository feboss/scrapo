import logging
from sqlite3 import Error
import sqlite3


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        logging.getLogger('DB create').error(e)
    return conn


def create_table(conn):
    create_table_query = """CREATE TABLE IF NOT EXISTS links (
        link TEXT PRIMARY KEY NOT NULL
    );"""
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_query)
    except Error as e:
        logging.getLogger('DB Table create').error(e)
    conn.commit()


def add_items(conn, values):
    cursor = conn.cursor()
    query = """INSERT OR IGNORE INTO links VALUES (?)"""
    executed = cursor.executemany(query, zip(values))
    conn.commit()
    query = """SELECT * FROM links ORDER BY rowid DESC LIMIT (?)"""
    cursor.execute(query, (executed.rowcount,))
    fetched_rows = cursor.fetchall()
    logging.getLogger('SQLITE3').info(
        "{} links inserted in DB".format(len(fetched_rows)))
    return [row[0] for row in fetched_rows]
