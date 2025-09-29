#!/usr/bin/env python3

import processes
import wikiparser
import config

schema = config.schema

db = processes.load_db_conn(config.dbname, config.user, config.host, config.password, schema)
tables = processes.load_tables(db, schema) # TODO - currently loads |entries as template, add check function?
api = processes.load_wiki_conn()

wiki = config.wiki # "calamitymod.wiki.gg"
page = config.page # "Wingman"
response = api.get_page_raw(wiki, page)

print(f"\n\nProcessing page: {wiki}, {page}\n\n")

wikiparser.process_page(db, tables, page, response.text)

print(db.list_tables(schema), '\n')

col_list = db.list_columns(schema, 'item infobox')
print(col_list, '\n')

print(db.select('item infobox', [item[0] for item in col_list]))

with db.conn.cursor() as cur:
    cur.execute(f"""SELECT constraint_name, constraint_type
    FROM information_schema.table_constraints
    WHERE table_schema = '{schema}'
    AND table_name = 'item infobox';""")
    print('\n\n\n', cur.fetchall())
