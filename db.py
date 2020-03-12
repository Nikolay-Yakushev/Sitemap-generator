# this module contains methods work with database

import yaml
import psycopg2


# connection to db function
def connect_db():
    # private database config
    with open('config_db.yaml', 'r') as config_db:
        data = yaml.load(config_db, Loader=yaml.FullLoader)
        conn = psycopg2.connect(
            database=data['database'],
            user=data['user'],
            password=data['password'],
            host=data['host'],
            port=data['port'])
        conn.set_session(autocommit=True)
    return conn


# function to check if table has already been created
def is_table(table_name):
    con = connect_db()
    cur = con.cursor()
    is_table = """select exists(select * 
                                from information_schema.tables 
                                where table_name=%s);"""
    cur.execute(is_table, (table_name,))
    if not cur.fetchone()[0]:
        table_create(table_name)
    con.close()


def table_create(table_name):
    con = connect_db()
    cur = con.cursor()
    table_crt = f"""create table {table_name} (url_parent text,
                                                    url_children text);"""
    cur.execute(table_crt)
    con.close()


# function that writes to database
# in the following format :
# url_parent  url_child
#  a             [b, c, d, f]
#  b             [h, j, k, l]
#  l             [q, w, e, r, t]
def write_db(table_name, data):
    con = connect_db()

    cur = con.cursor()

    url_ins = f"""insert into {table_name} (url_parent, url_children) values(%s, %s);"""

    # check if table exist
    is_table(table_name)
    # executemany method added
    cur.executemany(url_ins, (data.items()))
    con.close()


# drop table function
def delete_table(table_name):
    con = connect_db()
    drop_table = f"drop table {table_name}"
    cur = con.cursor()
    cur.execute(drop_table)
    con.close()
