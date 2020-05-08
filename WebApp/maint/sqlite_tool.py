import sqlite3
from sqlite3 import Error

    #create connection to database#
def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

    # create table function #
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

    #invoke sql query#
def invoke_query(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    return cur.lastrowid

    #read database#
def read_database(conn, sql):
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(sql)

    rows = cur.fetchall()
    return rows
        

def sqlite_api(db, sql, mode):
    conn = create_connection(db)
    with conn:
        if mode == 'read':
            data = read_database(conn, sql)
            objs = []
            for d in data:
                obj = {}
                keys= d.keys()
                for key in keys:
                    value = d[key]
                    obj[key] = value
                objs.append(obj)
            return objs
        elif mode == 'write':
            data = invoke_query(conn, sql)
            return data
    
    
        #CREATE TABLE#
    """
    sql = ''' CREATE TABLE IF NOT EXISTS items(
                                id integer PRIMARY KEY,
                                item_name text NOT NULL,
                                lubricant text NOT NULL,
                                app_method text NOT NULL,
                                capacity real NOT NULL,
                                points integer NOT NULL,
                                master_item text NOT NULL,
                                master_id text NOT NULL,
                                area text NOT NULL
                                ); '''

    if conn is not None:
        create_table(conn, sql_create_items_table)

        create_table(conn, sql_create_tasks_table)
    else:
        print(" Error! cannot create the database connection ")
    """
        
        #INSERT DATA#
    """
    with conn:
        sql = ''' INSERT INTO items(item_name, lubricant, app_method, capacity, points, master_item, master_id, area)
                VALUES(?,?,?,?,?,?,?,?)'''
        item = ('ELECTRIC MOTOR BEARINGS 2','POLY','G',0.00,2,'PUMP, HOT WATER REF PLUG WIPER #2','31-4-7855','TMP')
        invoke_query(conn, sql, item)
    """

    #UPDATE DATA#
    """
    with conn:
        sql= ''' UPDATE items
                SET item_name = 'ELECTRIC MOTOR BEARINGS 2'
                WHERE id = 2 '''
        record = ''
        invoke_query(conn, sql, record)
    """

    #DELETE DATA#
    """
    with conn:
        sql = ''' DELETE FROM items WHERE id=2 '''
        record = ''
        invoke_query(conn, sql, record)
    """

    #READ DATA#
    """
    with conn:
        sql = ''' SELECT * FROM items '''
        data = read_database(conn, sql)
        for d in data:
            keys= d.keys()
            for key in keys:
                value = d[key]
                print(key + " : {}".format(value))
        print(" ")
    """

"""
if __name__ == '__main__':
    database = "./test.db"
    
        #READ#
    sql = ''' SELECT * FROM items '''
    data = sqlite_api(database, sql, 'read')
    for d in data:
        print(d['item_name'])
        print(' ')

        #WRITE#
    #sql = ''' INSERT INTO items(item_name, lubricant,app_method, capacity, points, master_item, master_id, area)
    #            VALUES('Test item', 'poly', 'G', 0.00, 2, 'test master item', 'test master id', 'TMP') '''
    #data = sqlite_api(database, sql, 'write')
    #print(data)

    """
