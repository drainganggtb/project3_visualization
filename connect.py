import psycopg2
from config import config
import sys

def connect():
    conn = None
    try:
        params = config()
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        '''
        # create a cursor
        cur = conn.cursor()
        
        # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
        
        # close the communication with the PostgreSQL
        #cur.close()'''
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print('connectin successful')
    return conn
    '''finally:
        if conn is not None:
            conn.close()
            print('Database connection is closed')'''

if __name__ == '__main__':
    connect()