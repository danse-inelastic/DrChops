class MenuItem:

    def __init__(self, name, active=False, link='/', accesskey=''):
        self.name = name
        self.active = active
        self.link = link
        self.accesskey = accesskey
        return

    def activate(self): self.active = True; return self

    def deactivate(self): self.active = False; return self

    pass # end of MenuItem


class Menu:

    def __init__(self, items):
        self.items = items
        d = {}
        for item in items: d[item.name] = item
        self._name2item = d
        self.activeItem = items[0].activate()
        self.names = [ item.name for item in items ]
        return

    def activate(self, name):
        self.activeItem.deactivate()
        item = self._name2item[ name ]
        self.activeItem = item.activate()
        return

    pass # end of Menu

