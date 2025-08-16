#!/usr/bin/env python3

# import requests
import templatedata
import database_ops as dbops
import wikiparser
# import mwparserfromhell as mwp
# import psycopg2
import mwconnect
import config

db = dbops.DatabaseConnection()
conn = db.connect(config.dbname, config.user, config.host, config.password)

schema = config.schema # 'wikidb'
with conn.cursor() as cur:
    cur.execute("SET search_path TO %s", (schema,))

tables = templatedata.TableSet()

tabs = db.list_tables(schema)
print(tabs)
if tabs is not None:
    for tab in tabs:
        table_name = tab[0]
        tables.add_template(table_name)
        cols = db.list_columns(schema, table_name)
        print(cols)
        if cols is not None:
            for col in cols:
                column_name = col[0]
                tables.add_param(table_name, column_name)

for a, b in tables.data.items():
    op = a + ":"
    for c in b:
        op += " " + c
    print(op)

api = mwconnect.Connection()

wiki = config.wiki # "calamitymod.wiki.gg"
page = config.page # "Wingman"
response = api.get_page_raw(wiki, page)

print("\n\nCOMMENCING OPERATION\n\n")

wikiparser.process_page(db, tables, page, response.text)

print(db.list_tables(schema), '\n')
print(db.list_columns(schema, 'item infobox'), '\n')

with conn.cursor() as cur:
    cur.execute('select * from "item infobox"')
    a = cur.fetchall()
    print(a)




