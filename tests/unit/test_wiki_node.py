from wikiNode import WikiNode
import unittest
from hamcrest import *

class TestWikiNode(unittest.TestCase):
    def setUp(self):
       self.node = WikiNode('url','title','parent',['children'])
       child1 = WikiNode('child1url','child1title',self.node,None)
       child2 = WikiNode('child2url','child2title',self.node,None)

       child1_1 = WikiNode('child1_1url','child1_1title',child1,None)
       child1_2 = WikiNode('child1_2url','child1_2title',child1,None)

       child2_1 = WikiNode('child2_1url','child2_1title',child2,None)
       child2_2 = WikiNode('child2_2url','child2_2title',child2,None)

       child1.children = [child1_1, child1_2]
       child2.children = [child2_1, child2_2]
       self.node.children = [child1, child2]

    def test_str_returns_title(self):
        ''' Validating that the str() method of the WikiNode object is the title '''
        assert_that(str(self.node), is_(equal_to('title')))

    def test_iter_depth_first(self):

        # make sure it get child -> child1 -> child1_1 ->child1_2 ->child2 ->child2_1 ->child2_2
        # this is indended to be depth first algorithm
        # It probably makes more sense to write a depth first algorithm instead
        expected_list = [self.node,
                         self.node.children[0],
                         self.node.children[0].children[0],
                         self.node.children[0].children[1],
                         self.node.children[1],
                         self.node.children[1].children[0],
                         self.node.children[1].children[1]
        ]

        i = 0;
        for node in self.node:
            assert_that(node, is_(equal_to(expected_list[i])))
            i = i + 1

        ''' Create a second node equal to the first and validate the equality method '''
        # creating a second node and validating that it is equal to self.node
        node2 = WikiNode('url','title','parent',['children'])
        child1 = WikiNode('child1url','child1title',node2,None)
        child2 = WikiNode('child2url','child2title',node2,None)

        child1_1 = WikiNode('child1_1url','child1_1title',child1,None)
        child1_2 = WikiNode('child1_2url','child1_2title',child1,None)

        child2_1 = WikiNode('child2_1url','child2_1title',child2,None)
        child2_2 = WikiNode('child2_2url','child2_2title',child2,None)

        child1.children = [child1_1, child1_2]
        child2.children = [child2_1, child2_2]
        node2.children = [child1, child2]

        assert_that(self.node, is_(equal_to(node2)))


    def test_repr_returns_string(self):
        ''' Assure that __repr__ returns children correctly '''
        self.node.children[0].children = None
        self.node.children[1].children = None

        assert_that(repr(self.node), is_(equal_to('{} [{} {}, {} {}]'.format(self.node.title, self.node.children[0].title, 'None', self.node.children[1].title, 'None'))))

