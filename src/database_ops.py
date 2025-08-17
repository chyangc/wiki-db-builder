import psycopg2
from psycopg2 import sql

class DatabaseConnection:
    conn: psycopg2.extensions.connection

    def connect(self, dbname: str, user: str, host: str, password: str):
        try:
            conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' host='{host}' password='{password}'")
        except:
            raise ConnectionError("Failed to connect to the PostgreSQL Database.")
        print(f"Autocommit: {conn.autocommit} and Isolation Level: {conn.isolation_level}")
        self.conn = conn
        return conn

    # ---------------=====---------------=====---------------

    def add_table(self, name: str, cols: list[str]):
        with self.conn.cursor() as cur:
            scols = [
                sql.SQL("{} varchar(255)").format(sql.Identifier('|name'))
            ]
            scols += [sql.SQL("{} text").format(sql.Identifier(item)) for item in cols]
            # scols.insert(0, sql.SQL("{} text"))
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({fields});").format(
                table = sql.Identifier(name),
                fields = sql.SQL(',').join(scols)
            )
            cur.execute(query)
            # cur.execute("CREATE TABLE test (id integer, name text)")

    def add_col(self, table: str, name: str):
        with self.conn.cursor() as cur:
            query = sql.SQL("ALTER TABLE IF EXISTS {tab} ADD COLUMN {col} {type}").format(
                tab = sql.Identifier(table),
                col = sql.Identifier(name),
                type = sql.SQL('text'),
                # ?
            )
            cur.execute(query)
            # cur.execute("ALTER TABLE table_name ADD COLUMN new_column_name data_type [column_constraint]")

    def add_row(self, table: str, values: dict[str, str]):
        if not values:
            return

        with self.conn.cursor() as cur:
            query = sql.SQL("INSERT INTO {tab} ({fields}) VALUES ({items})").format(
                tab = sql.Identifier(table),
                fields = sql.SQL(',').join(map(sql.Identifier, values)),
                items = sql.SQL(',').join(map(sql.Placeholder, values))
            )
            cur.execute(query, values)
            # cur.execute("INSERT INTO test (a, b) VALUES (1, 'hi')")


    def set_value(self, table: str, col: str, val: str, condition: dict[str, str]): # ?
        pass

    def remove_rows(self, table: str, condition: dict[str, str]):
        pass

# ---------------=====---------------=====---------------

    def list_tables(self, schema: str):
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT tablename
                FROM pg_catalog.pg_tables
                WHERE schemaname = %s;
                """, (schema,)
            )
            return cur.fetchall()

    def list_columns(self, schema: str, table: str):
        with self.conn.cursor() as cur:
            cur.execute( # SELECT column_name, data_type, is_nullable, column_default
                """
                SELECT column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = %s
                AND table_name = %s;
                """, (schema, table)
            )
            return cur.fetchall()

    def select(self, table: str, columns: list[str]):
        with self.conn.cursor() as cur:
            query = sql.SQL("SELECT {cols} FROM {tab}").format(
                cols = sql.SQL(',').join(map(sql.Identifier, columns)),
                tab = sql.Identifier(table)
            )
            cur.execute(query)
            return cur.fetchall()


