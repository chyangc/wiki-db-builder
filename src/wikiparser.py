# import requests
# import templatedata
import database_ops as dbops
import mwparserfromhell as mwp
# import psycopg2

def process_page(db: dbops.DatabaseConnection, tables, title: str, content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates()
    # print(templates)
    for template in templates:
        process_template(db, tables, title, template)
    
    # TODO:
    # templates in templates -> postgres: link to entries in other tables
    # elsewhere:
    #   generator
    #   structure to input constants
    #   other settings e.g. filter templates
    #   retrieving data?


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







