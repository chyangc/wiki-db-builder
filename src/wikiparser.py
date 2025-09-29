# import requests
# import templatedata
import database_ops as dbops
import mwparserfromhell as mwp
# import psycopg2

def process_page(db: dbops.DatabaseConnection, tables, title: str, content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates(recursive=False)
    # print(templates)
    # for template in templates:
    #     process_template(db, tables, title, template)

    stack = [(template, None) for template in templates]
    while stack:
        item = stack.pop()
        id = process_template(db, tables, title, item[0], item[1])

        sub_templates = [a for b in [param.value.filter_templates() for param in item[0].params] for a in b]
        stack += [(sub_template, (id, item[0].name.strip())) for sub_template in sub_templates]


    #


def process_template(db: dbops.DatabaseConnection, tables, title: str, template: mwp.nodes.Template, container):
    # print(template.name)
    name = template.name.strip()
    a = tables.add_template(name)
    if a:
        db.add_template_table(name, [])

    vals: dict[str, str] = {
        dbops.TEMPLATE_PAGE: title,
    }
    if container:
        vals.setdefault(dbops.TEMPLATE_CONTAINER, container[0])
        vals.setdefault(dbops.TEMPLATE_CONTAINER_PARAM, container[1])
    
    for param in template.params:
        param_name = param.name.strip()
        b = tables.add_param(name, param_name)
        if b:
            db.add_col(name, param_name)
        
        vals.setdefault(param_name, param.value.strip())
    
    return db.add_entry(name, vals)







