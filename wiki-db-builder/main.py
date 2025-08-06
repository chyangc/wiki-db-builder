import requests
import templatedata
import database_ops as db
import wikiparser
# import mwparserfromhell as mwp
# import psycopg2
import config

schema = config.schema # 'wikidb'
conn = db.connect()

with conn.cursor() as cur:
    cur.execute("SET search_path TO %s", (schema,))

tables = templatedata.TableSet()

tabs = db.list_tables(conn, schema)
print(tabs)
if tabs is not None:
    for tab in tabs:
        table_name = tab[0]
        tables.add_template(table_name)
        cols = db.list_columns(conn, schema, table_name)
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




base = config.base # "https://{}/wiki/{}?action=raw"
wiki = config.wiki # "calamitymod.wiki.gg"
page = config.page # "Wingman"
url = base.format(wiki, page)
print(url)
response = requests.get(url)




print("\n\nCOMMENCING OPERATION\n\n")

wikiparser.process_page(conn, tables, page, response.text)

print(db.list_tables(conn, schema), '\n')
print(db.list_columns(conn, schema, 'item infobox'), '\n')

with conn.cursor() as cur:
    cur.execute('select * from "item infobox"')
    a = cur.fetchall()
    print(a)




