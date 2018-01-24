from window import TreeWindow
from wikiNode import WikiNode
import unittest
from hamcrest import *
from mock import MagicMock, patch, call

import gi
gi.require_version('Gtk', '3.0')

from gi.repository import Gtk

class TestWindow(unittest.TestCase):
    def setUp(self):
        # We don't want to mock everything in init and we don't want
        # Init to call all the Gtk methods, so patch it to do a NOP
        TreeWindow.__init__ = lambda x: None

        self.tw = TreeWindow()
        self.tw.node_lists = [[],[],[]]
        self.node_lists = [[WikiNode('url','test11'),WikiNode('url','test12')],
                           [WikiNode('url','test21'),WikiNode('url','test22')],
                           [WikiNode('url','test31'),WikiNode('url','test32')]]

    @patch('gi.repository.Gtk.Window.__init__')
    @patch('gi.repository.Gtk.Window.get_screen')
    @patch('gi.repository.Gtk.Window.resize')
    # Patching these so we don't try and call in to Gtk
    @patch('gi.repository.Gtk.Window.set_position')
    @patch('gi.repository.Gtk.Window.connect')
    def test_setup_main_window_calls_gtk_window_properly(self,mock_connect, mock_pos, mock_resize, mock_screen, mock_init):
        ''' These tests are going to be a bit convoluted
        We don't care so much what in Gtk we are calling (Gui tests may be better for that, though Gtk doesn't have selenium hooks afaik), instead we want to make sure any calculated values are getting generated properly'''
        # We don't want to mock everything in init and we don't want
        # Init to call all the Gtk methods, so patch it to do a NOP
        TreeWindow.__init__ = lambda x: None

        # The mocked screen object should return a static width and height
        mock_screen().get_width.return_value = 10
        mock_screen().get_height.return_value = 10
        self.tw.setup_main_window()

        # Leaving this here incase we decide to calculate the window title
        mock_init.assert_called_with(tw, title='Wiki Tree - root name')

        # Initial size should be width/2 by height/2
        mock_resize.assert_called_with(5,5)


    def test_setup_main_window_calls_gtk_window_properly(self):
        ''' Validate that the node lists are set up properly and that the grid lists are called the correct number of times '''
        self.tw.node_grid_lists = [MagicMock(), MagicMock(), MagicMock()]
        self.tw.set_node_lists(self.node_lists[0], self.node_lists[1], self.node_lists[2])

        # Verify the lists are set up properly
        assert_that(self.tw.node_lists, is_(equal_to(self.node_lists)))

        # Verify that we are clearing the GridLists once
        [gl.clear.assert_called_once() for gl in self.tw.node_grid_lists]

        # Check that each gridlist calls append for each of the entries in node_list
        for i in range(0,3):
            calls = [call.append([val.title]) for val in self.node_lists[i]]
            self.tw.node_grid_lists[i].assert_has_calls(calls)

    def test_toggle_tree_view_activated_handler_flips_handlers(self):
        ''' TODO '''
        assert_that(False,is_(equal_to(True)))
