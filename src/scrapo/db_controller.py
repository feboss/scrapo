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
    query = """CREATE TABLE IF NOT EXISTS links (link text NOT NULL UNIQUE);"""
    try:
        c = conn.cursor()
        c.execute(query)
    except Error as e:
        logging.getLogger('DB Table create').error(e)
    conn.commit()


def add_items(conn, values):
    c = conn.cursor()
    query = """INSERT OR IGNORE INTO links VALUES (?)"""
    c.executemany(query, zip(values))
    conn.commit()
    query = """SELECT * FROM links ORDER BY rowid DESC LIMIT (?)"""
    c.execute(query, (c.rowcount,))
    x = c.fetchall()
    logging.getLogger('SQLITE3').info(
        "{} links inserted in DB".format(len(x)))
    return [r[0] for r in x]
