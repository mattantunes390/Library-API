import logging
import pymysql


def conecta_banco():
    try:
        conn = pymysql.connect(host='127.0.0.1', user='localhost',
                               passwd='localhost', db='library',
                               charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        return conn, cur
    except pymysql.err.Error as excpt:
        logging.critical('%s', excpt)