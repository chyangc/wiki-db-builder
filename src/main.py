#!/usr/bin/env python3

import processes
import wikiparser
import config

schema = config.schema

db = processes.load_db_conn()
tables = processes.load_tables(db, schema)
api = processes.load_wiki_conn()

wiki = config.wiki # "calamitymod.wiki.gg"
page = config.page # "Wingman"
response = api.get_page_raw(wiki, page)

print("\n\nCOMMENCING OPERATION\n\n")

wikiparser.process_page(db, tables, page, response.text)

print(db.list_tables(schema), '\n')
print(db.list_columns(schema, 'item infobox'), '\n')

with db.conn.cursor() as cur:
    cur.execute('select * from "item infobox"')
    a = cur.fetchall()
    print(a)




