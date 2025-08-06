import mwparserfromhell as mwp
import templatedata as tpd

# data = tpd.DataField()

def process_page(content: str):
    wkt = mwp.parse(content)
    templates = wkt.filter_templates()
    # print(templates)

    data: list[tpd.TemplateData] = []

    for template in templates:
        process_template(template)

    for temp in data:
        print(f"\n{temp.name}")
        for arg in temp.args:
            print(f" - {arg}")
    
    return data

def process_template(template: mwp.nodes.Template):
    print(template.name)

    item = tpd.TemplateData(template.name.strip()) # str(template.name))
    for param in template.params:
        item.add_param(param.name.strip())

    # data.append(item)






