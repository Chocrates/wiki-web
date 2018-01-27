from spider import Spider

import logging
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')

from gi.repository import Gtk, WebKit2, Gdk

# Move this to a file when it gets too big
CSS = b'''
.clicked {
   color: red;
   background-color: red;
}

.bread-crumb {
   color: orange;
   background-color: orange;
}
'''


class TreeWindow(Gtk.Window):
    def __init__(self, wiki_node):
        self.logger = logging.getLogger('Wiki-web.window.TreeWindow')
        self.setup_main_window()
        self.set_style(CSS)
        menu_grid = self.setup_widget_layout()
        self.setup_initial_lists(wiki_node)
        self.setup_inital_trees(menu_grid)
        self.render_web_kit(wiki_node.base_url)

    def setup_main_window(self):
        ''' Set up the main window details '''
        Gtk.Window.__init__(self, title='Wiki Tree - root name')
        self.set_border_width(10)
        self.resize(self.get_screen().get_width() / 2,
                    self.get_screen().get_height() / 2)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect('delete-event', Gtk.main_quit)

    def setup_widget_layout(self):
        ''' Defines the widget layout and returns a reference to the
        grid widget '''
        # All of the content will be rendered inside an encapsulating box
        # Apparently self.window can only accept a single widget
        # This parent box will tile all sub-widgets horizontall
        # This will allow us to have a vertical menu and then tile the web-content
        # next to it
        outer_box = Gtk.Box(
            orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.add(outer_box)

        # Create grid to contain the navigation 
        menu_grid = Gtk.Grid()
        menu_grid.set_column_homogeneous(True) # All columns have the same width
        menu_grid.set_row_homogeneous(True) # All rows have the same height
        outer_box.pack_start(menu_grid, False, False, 10) # Put the grid in our main box
                                                        # Taking up only as much space as it needs

        # Create the webkit widget and pack it in our main widget
        ctx = WebKit2.WebContext.get_default()
        self.web_view = WebKit2.WebView.new_with_context(ctx)
        self.web_view.connect('load-changed', self.load_changed)
        self.web_view.connect('load-failed', self.load_failed)
        outer_box.pack_start(self.web_view, True, True, 10)

        return menu_grid

    def set_node_lists(self,node_zero_list,node_one_list,node_two_list):
        self.node_lists[0] = node_zero_list
        self.node_lists[1] = node_one_list
        self.node_lists[2] = node_two_list

        [child.clear() for child in self.node_grid_lists]

        [self.node_grid_lists[0].append([node.title]) for node in node_zero_list]
        [self.node_grid_lists[1].append([node.title]) for node in node_one_list]
        [self.node_grid_lists[2].append([node.title]) for node in node_two_list]

    def reset_root_node(self,node):
        ''' Set up the columns for the root node '''
        # Each column needs a list of nodes to be displayed
        # And their string representation in a Gtk ListStore
        self.set_node_lists([node],node.children,[])

    def setup_initial_lists(self, node):
        ''' Setup the intiial node lists
        They all need to be in the objects scope so they can
        Mutated by UI callbacks later
        TODO: Can I make them immutable?  Would that save me any headaches?'''

        # Initialize our Grid Lists
        self.node_grid_lists = [Gtk.ListStore(str),Gtk.ListStore(str),Gtk.ListStore(str)]
        self.node_lists = [[],[],[]]
        self.reset_root_node(node)

    def setup_inital_trees(self, menu_grid):
        ''' Put together our tree views
        These will display our grid lists and be put in our grid in order'''

        # Set up the left most root tree view with the node 0 list
        self.tree_views = []
        self.tree_views.append(Gtk.TreeView.new_with_model(self.node_grid_lists[0]))

        # Grid's aren't usually supposed to be buttons
        # So we need to let me fire an event on a single click instead of double click
        self.tree_views[0].set_activate_on_single_click(True)

        # Setup the column and title
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Node0', renderer, text=0)
        self.tree_views[0].append_column(column)

        # Add a scrollbar to our treeview for pages with lots of links
        scrollable_treelist0 = Gtk.ScrolledWindow()
        scrollable_treelist0.add(self.tree_views[0])

        # Attach the treeview (now hidden in a scrollable) to the menugrid
        # And give it a width
        menu_grid.attach(scrollable_treelist0, 0, 0, 200, 10)

        self.tree_views.append(Gtk.TreeView.new_with_model(self.node_grid_lists[1]))
        self.tree_views[1].set_activate_on_single_click(True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Node1', renderer, text=0)
        self.tree_views[1].append_column(column)
        scrollable_treelist1 = Gtk.ScrolledWindow()
        scrollable_treelist1.add(self.tree_views[1])
        menu_grid.attach_next_to(scrollable_treelist1,
                                    scrollable_treelist0,
                                    Gtk.PositionType.RIGHT, 200, 10)

        self.tree_views.append(Gtk.TreeView.new_with_model(self.node_grid_lists[2]))
        self.tree_views[2].set_activate_on_single_click(True)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn('Node2', renderer, text=0)
        self.tree_views[2].append_column(column)
        scrollable_treelist2 = Gtk.ScrolledWindow()
        scrollable_treelist2.add(self.tree_views[2])
        menu_grid.attach_next_to(scrollable_treelist2,
                                    scrollable_treelist1,
                                    Gtk.PositionType.RIGHT, 200, 10)

        # Finally connect all the "buttons" to their event handlers
        self.tree_view_signal_ids = []
        self.tree_view_signal_ids.append(self.tree_views[0].connect(
            'row-activated', self.node_zero_selection))

        self.tree_view_signal_ids.append(self.tree_views[1].connect(
            'row-activated', self.node_one_selection))

        self.tree_view_signal_ids.append(self.tree_views[2].connect(
            'row-activated', self.node_two_selection))

        # Set initial blocked toggle to false
        # This will be used later to determine if the
        # Listeners above are blocked or unblocked when
        # We update their backing lists
        self.signals_blocked = False 

    def toggle_tree_view_activated_handler(self):
        ''' Toggle block on treeView signals '''
        if self.signals_blocked:
            for i in range(0,len(self.tree_views)):
                self.tree_views[i].handler_unblock(self.tree_view_signal_ids[i])
        else:
            for i in range(0,len(self.tree_views)):
                self.tree_views[i].handler_block(self.tree_view_signal_ids[i])

        self.signals_blocked = not self.signals_blocked

    def node_zero_selection(self, tree_view, path, column):
        ''' Event handler for list items in the node 0 grid '''
        try:
            # Block event handlers so we don't fire as we update them
            self.toggle_tree_view_activated_handler()

            # Grab the curent selected node
            row_num = tree_view.get_cursor()[0].get_indices()

            # Find the node from our 
            node = [
                x for x in self.node_lists[0]
                if x.title == tree_view.get_model()[row_num][0]
            ][0]
            self.logger.debug('Selected Node: ' + node.title)
            spider = Spider()

            # Build our node out only if we don't have children
            if node.children is None:
                node = spider.build_node(node.base_url, node.parent, 1)

            # If this is the root node 
            if node.parent is None:
                self.reset_root_node(node)
            # If this is node's parent is root, we can't set its peers
            elif node.parent.parent is None:
                self.set_node_lists(node.parent,node.parent.children,node.children)

            # If this node's parent has peers (IE its parent has a parent with chidlren)
            # We set the children to be the node0 list
            else:
                self.set_node_lists(node.parent.parent.children, node.parent.children, node.children)

            self.render_web_kit(node.base_url)
            self.tree_views[0].set_cursor(row_num)
            self.toggle_tree_view_activated_handler()

        except Exception as e:
            self.logger.error(e)

    def node_one_selection(self, tree_view, path, column):
        ''' Event handler for list items in the node 1 grid '''
        # Block event handlers so we don't fire as we update them
        self.toggle_tree_view_activated_handler()

        row_num = tree_view.get_cursor()[0].get_indices()
        node = [
            x for x in self.node_lists[1]
            if x.title == tree_view.get_model()[row_num][0]
        ][0]
        spider = Spider()
        self.logger.debug('Selected Node: ' + node.title)
        node = spider.build_node(node.base_url, node.parent, 1)

        self.set_node_lists(self.node_lists[0],self.node_lists[1],node.children)

        self.render_web_kit(node.base_url)

        self.tree_views[1].set_cursor(row_num)

        self.toggle_tree_view_activated_handler()

    def node_two_selection(self, tree_view, path, column):
        ''' Event handler for list items in the node 2 grid '''
        # Block event handlers so we don't fire as we update them
        self.toggle_tree_view_activated_handler()

        row_num = tree_view.get_cursor()[0].get_indices()
        node = [
            x for x in self.node_lists[2]
            if x.title == tree_view.get_model()[row_num][0]
        ][0]

        self.logger.debug('Selected Node: ' + node.title)

        spider = Spider()

        if node.children is None:
            node = spider.build_node(node.base_url, node.parent, 1)

        self.set_node_lists(self.node_lists[1], self.node_lists[2], node.children)

        self.tree_views[1].set_cursor(row_num)

        self.render_web_kit(node.base_url)

        self.toggle_tree_view_activated_handler()

    def render_web_kit(self, url):
        self.logger.debug('Rendering URL: ' + url)
        # Load Url
        spider = Spider()
        self.web_view.load_uri(url)
        self.show_all()

    def load_changed(self, web_view, evt):
        if evt == WebKit2.LoadEvent.FINISHED:
            _title = web_view.get_title() or ''
            self.set_title(web_view.get_title() or '')
        else:
            self.set_title('Loading... {:0.1f}%'.format(
                web_view.get_estimated_load_progress()))

    def load_failed(self, web_view, evt, url, error):
        self.logger.error('Error loading url: %s - %s', url, error)

    def set_style(self, css):
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
