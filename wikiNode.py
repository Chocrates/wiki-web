class WikiNode:
    def __init__(self, baseUrl,title, parent=None, children=None):
        self.baseUrl = baseUrl
        self.parent = parent
        self.children = children
        self.title = title

    def __iter__(self):
        if self.children is not None:
            return iter([self.baseUrl] +  [iter(child) for child in self.children if child is not None])
        else:
            return iter([self.baseUrl])
