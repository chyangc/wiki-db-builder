import requests
import templatedata
import database_ops as db
# import wikiparser
import mwparserfromhell as mwp
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


# ---

def process_page(title: str, content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates()
    # print(templates)
    for template in templates:
        process_template(title, template)
    
    # TODO:
    # templates in templates -> postgres: link to entries in other tables
    # elsewhere:
    #   generator
    #   structure to input constants
    #   other settings e.g. filter templates
    #   retrieving data?


def process_template(title: str, template: mwp.nodes.Template):
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

    # data.append(item)


print("\n\nCOMMENCING OPERATION\n\n")

process_page(item, response.text)

print(db.list_tables(conn, 'public'))
print(db.list_columns(conn, 'public', 'wingman'))

with conn.cursor() as cur:
    cur.execute('select * from "item infobox"')
    a = cur.fetchall()
    print(a)




