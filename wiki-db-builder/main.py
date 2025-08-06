import requests
import templatedata
import database_ops as db
import wikiparser
# import mwparserfromhell as mwp
# import psycopg2

base = "https://{}/wiki/{}?action=raw"
wiki = "calamitymod.wiki.gg"
item = "Wingman"
url = base.format(wiki, item)
print(url)

response = requests.get(url)
# print(response)
# wikiparser.process_page(response.text)

tables = templatedata.TableSet()
conn = db.connect()
tabs = db.list_tables(conn, 'public')
print(tabs)
if tabs is not None:
    for tab in tabs:
        table_name = tab[0]
        tables.add_template(table_name)
        cols = db.list_columns(conn, 'public', table_name)
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


print("\n\nCOMMENCING OPERATION\n\n")

wikiparser.process_page(conn, tables, item, response.text)

print(db.list_tables(conn, 'public'), '\n')
print(db.list_columns(conn, 'public', 'item infobox'), '\n')

with conn.cursor() as cur:
    cur.execute('select * from "item infobox"')
    a = cur.fetchall()
    print(a)




