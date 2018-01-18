
class WikiNode:
    def __init__(self, baseUrl, title, parent=None, children=None):
        self.baseUrl = baseUrl
        self.parent = parent
        self.children = children
        self.title = title

    def __str__(self):
        return self.title

    def __iter__(self):
        ''' Implements a recursive depth first
        traversal of the list of nodes '''
        yield self
        for child in self.children:
            for node in child:  # calls the iter on the child
                yield node
