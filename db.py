import psycopg2


def db_connection():
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        dbname='library',
        user='postgres',
        password='02062002'
    )
    return conn
