#!/usr/bin/env python3

import processes
import wikiparser
import config

schema = config.schema

db = processes.load_db_conn(config.dbname, config.user, config.host, config.password, schema)
tables = processes.load_tables(db, schema) # TODO - currently loads |entries as template, add check function?
api = processes.load_wiki_conn()

def test_page_raw():
    wiki = config.wiki # "calamitymod.wiki.gg"
    page = config.page # "Wingman"
    response = api.get_page_raw(wiki, page)

    print(f"\n\nProcessing page: {wiki}, {page}\n\n")

    wikiparser.process_page(db, tables, page, response.text)

def test_page_api():
    wiki = config.wiki_api # "https://calamitymod.wiki.gg/api.php"
    page = config.page # "Wingman"
    response = api.get_page(wiki, page)

    print(f"\n\nProcessing page: {wiki}, {page}\n\n")

    wikiparser.process_page(db, tables, page, response.text)

def print_db_test(table: str):
    print(db.list_tables(schema), '\n')

    col_list = db.list_columns(schema, table)
    print(col_list, '\n')

    print(db.select(table, [item[0] for item in col_list]))

    with db.conn.cursor() as cur:
        cur.execute(f"""SELECT constraint_name, constraint_type
        FROM information_schema.table_constraints
        WHERE table_schema = '{schema}'
        AND table_name = '{table}';""")
        print('\n\n\n', cur.fetchall())

test_page_raw()
print_db_test('item infobox')

test_page_api()
print_db_test('item infobox\\n')

