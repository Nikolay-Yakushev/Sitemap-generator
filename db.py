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
    if cur.fetchone()[0]:
        return True
    con.close()

# function that writes to database
# in the following format :
# url_parent  url_child
#  a             b
#  a             c
#  b             d
#  b             e
def write_db(table_name, url_parent, url_child):
    con = connect_db()

    cur = con.cursor()
    table_crt = f"""create table {table_name} (url_parent text,
                                                url_child text);"""

    url_ins = """insert into urls (url_parent, url_child) values(%s, %s);"""

    result = is_table(table_name)
    if not result:
        # if table does not exist create it and write data
        cur.execute(table_crt)
        cur.execute(url_ins, (url_parent, url_child,))
    else:
        cur.execute(url_ins, (url_parent, url_child,))
    con.close()


# drop table function
def delete_table(table_name):
    con = connect_db()
    drop_table = f"drop table {table_name}"
    cur = con.cursor()
    # if script starts again
    # delete_table function will
    # drop table created in previous iteration
    result = is_table(table_name)
    if result:
        cur.execute(drop_table)
    con.close()
