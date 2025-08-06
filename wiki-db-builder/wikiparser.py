# import requests
# import templatedata
import database_ops as db
import mwparserfromhell as mwp
# import psycopg2

def process_page(conn, tables, title: str, content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates()
    # print(templates)
    for template in templates:
        process_template(conn, tables, title, template)
    
    # TODO:
    # templates in templates -> postgres: link to entries in other tables
    # elsewhere:
    #   generator
    #   structure to input constants
    #   other settings e.g. filter templates
    #   retrieving data?


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

    # data.append(item)






