class WikiNode:
    def __init__(self, base_url, title, parent=None, children=None):
        self.base_url = base_url
        self.parent = parent
        self.children = children
        self.title = title

    def __str__(self):
        return self.title

    def __iter__(self):
        ''' Implements a recursive depth first
        traversal of the list of nodes '''
        yield self
        if self.children is not None:
            for child in self.children:
                for node in child:  # calls the iter on the child
                    yield node

    def __eq__(self, node):
        return (self.base_url == node.base_url and 
            self.children == node.children and
            self.title == node.title)

    def __repr__(self):
        return '{} {}'.format( self.title , repr(self.children))
