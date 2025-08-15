import templatedata
import database_ops as db
# import wikiparser
import mwconnect

import mwparserfromhell as mwp
import config

def load_db_conn():
    conn = db.connect(config.dbname, config.user, config.host, config.password)

    schema = config.schema # 'wikidb'
    with conn.cursor() as cur:
        cur.execute("SET search_path TO %s", (schema,))
    
    return conn

def load_tables(conn, schema):
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
    
    return tables


def load_wiki_conn():
    api = mwconnect.Connection()
    return api
# ?

def get_page(api, conn, tables, schema):
    wiki = config.wiki # "calamitymod.wiki.gg"
    page = config.page # "Wingman"
    response = api.get_page_raw(wiki, page)

    process_page(conn, tables, page, response.text)

    print(db.list_tables(conn, schema), '\n')
    print(db.list_columns(conn, schema, 'item infobox'), '\n')

    with conn.cursor() as cur:
        cur.execute('select * from "item infobox"')
        a = cur.fetchall()
        print(a)




# ---- from wikiparser ----

def process_page(conn, tables, title: str, content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates()
    # print(templates)
    for template in templates:
        process_template(conn, tables, title, template)


def process_template(conn, tables, title: str, template: mwp.nodes.Template):
    # print(template.name)
    with conn.cursor() as cur:
        try:
            name = template.name.strip()
            a = tables.add_template(name)
            if a:
                db.add_table(cur, name, [])

            vals = {'|name': title}
            for param in template.params:
                param_name = param.name.strip()
                b = tables.add_param(name, param_name)
                if b:
                    db.add_col(cur, name, param_name)
                
                vals.setdefault(param_name, param.value.strip())
            
            db.add_row(cur, name, vals)
        except Exception as error: # (Exception, psycopg2.DatabaseError) as error:
            print(error)






