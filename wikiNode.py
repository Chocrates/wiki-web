class WikiNode:
    def __init__(self, baseUrl, children, rawPageBody):
        self.baseUrl = baseUrl
        self.children = children
        self.rawPageBody = rawPageBody

    def __iter__(self):
        if self.children is not None:
            return iter([self.baseUrl] +  [iter(child) for child in self.children if child is not None])
        else:
            return iter([self.baseUrl])
