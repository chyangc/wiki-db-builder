import templatedata
import database_ops as dbops
# import wikiparser
import mwconnect

import mwparserfromhell as mwp
import config

def load_db_conn():
    db = dbops.DatabaseConnection()
    conn = db.connect(config.dbname, config.user, config.host, config.password)

    schema = config.schema # 'wikidb'
    with conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema,))
    
    return conn

def load_tables(db, schema):
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
    
    return tables


def load_wiki_conn():
    api = mwconnect.Connection()
    return api
# ?
# ?
def get_page(api, db: dbops.DatabaseConnection, tables, schema):
    wiki = config.wiki # "calamitymod.wiki.gg"
    page = config.page # "Wingman"
    response = api.get_page_raw(wiki, page)

    process_page(db, tables, page, response.text)

    print(db.list_tables(schema), '\n')
    print(db.list_columns(schema, 'item infobox'), '\n')

    with db.conn.cursor() as cur:
        cur.execute('select * from "item infobox"')
        a = cur.fetchall()
        print(a)




# ---- from wikiparser ----

def process_page(db: dbops.DatabaseConnection, tables, title: str, content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates()
    # print(templates)
    for template in templates:
        process_template(db, tables, title, template)


def process_template(db: dbops.DatabaseConnection, tables, title: str, template: mwp.nodes.Template):
    # print(template.name)
    name = template.name.strip()
    a = tables.add_template(name)
    if a:
        db.add_table(name, [])

    vals = {'|name': title}
    for param in template.params:
        param_name = param.name.strip()
        b = tables.add_param(name, param_name)
        if b:
            db.add_col(name, param_name)
        
        vals.setdefault(param_name, param.value.strip())
    
    db.add_row(name, vals)






