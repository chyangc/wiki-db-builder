
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

