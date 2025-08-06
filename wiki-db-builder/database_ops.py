import sys
import psycopg2
from psycopg2 import sql

# conn: psycopg2.extensions.connection

def connect():
    try:
        conn = psycopg2.connect("dbname='wikidata' user='wikireader' host='localhost' password='test'")
    except:
        print("I am unable to connect to the database")
        sys.exit()
    print(f"Autocommit: {conn.autocommit} and Isolation Level: {conn.isolation_level}")
    return conn

def stuff(conn):
    with conn.cursor() as cur:
        try:
            cur.execute("SELECT version()") # simple single row system query
            single_row = cur.fetchone() # returns a single row as a tuple
            print(f"{single_row}") # use an f-string to print the single tuple returned

            # cur.execute("CREATE TABLE test (id integer, name text)")
            add_table(cur, 'test', ['id', 'name'])
            print(list_columns(conn, "public", 'test'))

            cur.execute("INSERT INTO test VALUES (1, 'hi')")
            cur.execute("INSERT INTO test VALUES (2, 'hello')")
            add_row(cur, 'test', {'id': 'num', 'name': 'ok'})

            cur.execute("SELECT * FROM test")
            many_rows = cur.fetchmany(5)
            print(*many_rows, sep = "\n")
            print()

            rt = list_tables(conn, "public")
            print(rt)

            print("\n\n----======----\n\n")

            add_table(cur, 'another', [])
            print(list_tables(conn, 'public'))
            print(list_columns(conn, 'public', 'another'))
            add_col(cur, 'another', 'hi')
            add_row(cur, 'another', {'hi': 'asd'})
            cur.execute("SELECT * FROM another")
            res = cur.fetchall()
            print(res)

        # a more robust way of handling errors
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

# ---------------=====---------------=====---------------

def list_tables(conn, schema: str):
    with conn.cursor() as cur:
        try:
            cur.execute(
                """
                SELECT tablename
                FROM pg_catalog.pg_tables
                WHERE schemaname = %s;
                """, (schema,)
            )
            return cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

def list_columns(conn, schema: str, table: str):
    with conn.cursor() as cur:
        try:
            cur.execute( # SELECT column_name, data_type, is_nullable, column_default
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s
                AND table_name = %s;
                """, (schema, table)
            )
            return cur.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


def add_table(cur, name: str, cols: list[str]):
    scols = [sql.SQL("{} varchar(255)").format(sql.Identifier('|name'))]
    scols += [sql.SQL("{} text").format(sql.Identifier(item)) for item in cols]
    # scols.insert(0, sql.SQL("{} text"))
    query = sql.SQL("CREATE TABLE {table} ({fields});").format(
        table = sql.Identifier(name),
        fields = sql.SQL(',').join(scols)
    )
    cur.execute(query)
    # cur.execute("CREATE TABLE test (id integer, name text)")

def add_col(cur, table: str, name: str):
    query = sql.SQL("ALTER TABLE {tab} ADD COLUMN {col} {type}").format(
        tab = sql.Identifier(table),
        col = sql.Identifier(name),
        type = sql.SQL('text'),
        # ?
    )
    cur.execute(query)
    # cur.execute("ALTER TABLE table_name ADD COLUMN new_column_name data_type [column_constraint]")

def add_row(cur, table: str, values: dict[str, str]):
    if not values:
        return

    keys = []; vals = []; plh = []
    for k, v in values.items():
        keys.append(sql.Identifier(k))
        vals.append(v)
        plh.append(sql.Placeholder())
    
    query = sql.SQL("INSERT INTO {tab} ({fields}) VALUES ({items})").format(
        tab = sql.Identifier(table),
        fields = sql.SQL(',').join(keys),
        items = sql.SQL(',').join(plh)
    )
    cur.execute(query, tuple(vals))
    # cur.execute("INSERT INTO test (a, b) VALUES (1, 'hi')")


def set_value(table: str, col: str, val: str, condition: dict[str, str]): # ?
    pass

def remove_rows(table: str, condition: dict[str, str]):
    pass


# conn = connect()
# stuff(conn)