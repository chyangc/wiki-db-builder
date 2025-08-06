
class TemplateData:
    name: str
    args: set[str] = set()

    def __init__(self, name: str):
        self.name = name

    def has(self, x: str):
        return x in self.args

    def add_param(self, x: str):
        self.args.add(x)

    #

class DataField:
    templates: dict[str, TemplateData] = dict()

    def has(self, name: str):
        return name in self.templates

    def get(self, name: str):
        return self.templates.get(name)

    def add_template(self, name: str):
        return self.templates.setdefault(name, TemplateData(name))
    
    def add_param(self, name: str, x: str):
        self.templates[name].add_param(x)

    def check_template(self, name: str):
        pass

    def check_param(self, name: str, x: str):
        pass

    #

class TableSet:
    data: dict[str, set[str]] = dict()

    def set_data(self, data: dict[str, set[str]]) -> None:
        self.data = data

    def has_template(self, name: str) -> bool:
        return name in self.data

    def has_param(self, name: str, param: str) -> bool:
        if not self.has_template(name):
            return False
        return param in self.data[name]

    def add_template(self, name: str) -> bool:
        if self.has_template(name):
            return False
        self.data.setdefault(name, set())
        return True
    
    def add_param(self, name: str, param: str) -> bool:
        if not self.has_template(name) or self.has_param(name, param):
            return False
        self.data[name].add(param)
        return True

    def add_both(self, name: str, param: str) -> tuple[bool, bool]:
        a = self.add_template(name)
        b = self.add_param(name, param)
        return (a, b)

    #

'''
class ItemTemplate:
    name: str
    base: TemplateData
    data: dict[str, str] = dict()

    def __init__(self, name: str, base: TemplateData) -> None:
        self.name = name
        self.base = base

    def add_value(self, k: str, v: str):
        if k not in self.base.args:
            self.base.add_param(k)
        self.data.setdefault(k, v)

    #

class WikiItem:
    name: str
    data: dict[str, ItemTemplate] = dict()

    #
'''