import psycopg2
from psycopg2 import sql

ENTRY_TABLE = '|entries'
ENTRY_ID = 'id'
ENTRY_TEMPLATE = 'template'

TEMPLATE_ID = '|id'
TEMPLATE_PAGE = '|page'
TEMPLATE_ENTRY_ID = '|entry'
TEMPLATE_CONTAINER = '|container'
TEMPLATE_CONTAINER_PARAM = '|container_param'

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

    def setup(self, schema):
        with self.conn.cursor() as cur:
            cur.execute("SET search_path TO %s", (schema,))
            self.add_table(ENTRY_TABLE, [
                sql.SQL("{} serial primary key").format(sql.Identifier(ENTRY_ID)),
                sql.SQL("{} varchar(255)").format(sql.Identifier(ENTRY_TEMPLATE)),
            ])

    # ---------------=====---------------=====---------------

    def add_template_table(self, name: str, cols: list[str]):
        scols = [
            sql.SQL("{} serial primary key").format(sql.Identifier(TEMPLATE_ID)),
            sql.SQL("{} varchar(255)").format(sql.Identifier(TEMPLATE_PAGE)),
            sql.SQL("{} integer references {} ({})").format(sql.Identifier(TEMPLATE_ENTRY_ID), sql.Identifier(ENTRY_TABLE), sql.Identifier(ENTRY_ID)),
            sql.SQL("{} integer references {} ({})").format(sql.Identifier(TEMPLATE_CONTAINER), sql.Identifier(ENTRY_TABLE), sql.Identifier(ENTRY_ID)),
            sql.SQL("{} varchar(255)").format(sql.Identifier(TEMPLATE_CONTAINER_PARAM)),
        ]
        scols += [sql.SQL("{} text").format(sql.Identifier(item)) for item in cols]
        self.add_table(name, scols)

    def add_entry(self, table: str, values: dict[str, str]):
        # values.setdefault(TEMPLATE_PAGE, title)
        id = self.add_row(ENTRY_TABLE, {ENTRY_TEMPLATE: table}, ENTRY_ID)
        id = id[0] if id else None
        values.setdefault(TEMPLATE_ENTRY_ID, str(id))
        # if container:
        #     values.setdefault(TEMPLATE_CONTAINER, str(container))
        self.add_row(table, values)
        return id

    # ---------------=====---------------=====---------------

    def add_table(self, name: str, cols: list[sql.Composed]):
        with self.conn.cursor() as cur:
            query = sql.SQL("CREATE TABLE IF NOT EXISTS {table} ({fields})").format(
                table = sql.Identifier(name),
                fields = sql.SQL(',').join(cols)
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

    def add_row(self, table: str, values: dict[str, str] = {}, returning: str = ''):
        with self.conn.cursor() as cur:
            query = sql.SQL("INSERT INTO {} ").format(sql.Identifier(table))
            if values:
                query += sql.SQL("({fields}) VALUES ({items})").format(
                    fields = sql.SQL(',').join(map(sql.Identifier, values)),
                    items = sql.SQL(',').join(map(sql.Placeholder, values))
                )
            else:
                query += sql.SQL("DEFAULT VALUES")
            
            if returning:
                query += sql.SQL(" RETURNING {}").format(sql.Identifier(returning))
            cur.execute(query, values)
            # cur.execute("INSERT INTO test (a, b) VALUES (1, 'hi')")
            if returning:
                return cur.fetchone()


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
                cols = sql.SQL(',').join(map(sql.Identifier, columns)) if columns else sql.SQL('*'),
                tab = sql.Identifier(table),
            )
            cur.execute(query)
            return cur.fetchall()


