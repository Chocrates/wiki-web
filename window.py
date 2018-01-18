import gi
gi.require_version('Gtk','3.0')
gi.require_version('WebKit2','4.0')
from gi.repository import Gtk, WebKit2, Gdk
import math
from wikiNode import WikiNode
import cairo
from spider import Spider
import logging

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
   def __init__(self, wikiNode):
      self.logger = logging.getLogger('Wiki-web.window.TreeWindow')
      self.logger.debug("init method")
      #import pdb; pdb.set_trace()
      Gtk.Window.__init__(self, title='Wiki Tree - root name')
      self.set_style(CSS)

      # Set the root node
      self.node = wikiNode

      self.set_border_width(10)
      self.resize(self.get_screen().get_width()/2,self.get_screen().get_height()/2)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.connect('delete-event', Gtk.main_quit)

      self.outerBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
      self.add(self.outerBox)

      # Create the box to contain the buttons
      self.urlGrid = Gtk.Grid()
      self.urlGrid.set_column_homogeneous(True)
      self.urlGrid.set_row_homogeneous(True)
      #self.urlBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
      self.outerBox.pack_start(self.urlGrid,False,False,10)

      # Create HTML Box for the webkit widget
      self.webBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=6)
      self.outerBox.pack_start(self.webBox,True,True,10)
      ctx = WebKit2.WebContext.get_default()
      self.webView = WebKit2.WebView.new_with_context(ctx)
      self.webView.connect('load-changed', self.load_changed)
      self.webView.connect('load-failed', self.load_failed)
      self.webBox.pack_start(self.webView,True,True,0)

      # Set the starting lists
      self.node0List = [wikiNode]
      self.node0GridList = Gtk.ListStore(str)
      self.node0GridList.append([wikiNode.title])

      self.node1List = wikiNode.children
      self.node1GridList = Gtk.ListStore(str)
      [self.node1GridList.append([child.title]) for child in wikiNode.children]

      self.node2List = [] # Initialize empty
      self.node2GridList = Gtk.ListStore(str)

      self.treeView0 = Gtk.TreeView.new_with_model(self.node0GridList)
      self.treeView0.set_activate_on_single_click(True)
      renderer = Gtk.CellRendererText()
      column = Gtk.TreeViewColumn('Node0',renderer, text=0)
      self.treeView0.append_column(column)
      self.scrollable_treelist0 = Gtk.ScrolledWindow()
      self.scrollable_treelist0.add(self.treeView0)
      self.urlGrid.attach(self.scrollable_treelist0, 0 ,0,200,10)

      self.treeView1 = Gtk.TreeView.new_with_model(self.node1GridList)
      self.treeView1.set_activate_on_single_click(True)
      renderer = Gtk.CellRendererText()
      column = Gtk.TreeViewColumn('Node1',renderer, text=0)
      self.treeView1.append_column(column)
      self.scrollable_treelist1 = Gtk.ScrolledWindow()
      self.scrollable_treelist1.add(self.treeView1)
      self.urlGrid.attach_next_to(self.scrollable_treelist1,self.scrollable_treelist0,Gtk.PositionType.RIGHT, 200,10)

      self.treeView2 = Gtk.TreeView.new_with_model(self.node2GridList)
      self.treeView2.set_activate_on_single_click(True)
      renderer = Gtk.CellRendererText()
      column = Gtk.TreeViewColumn('Node2',renderer, text=0)
      self.treeView2.append_column(column)
      self.scrollable_treelist2 = Gtk.ScrolledWindow()
      self.scrollable_treelist2.add(self.treeView2)
      self.urlGrid.attach_next_to(self.scrollable_treelist2, self.scrollable_treelist1,Gtk.PositionType.RIGHT,200,10)

      self.renderWebKit(wikiNode.baseUrl)

      self.treeView0SignalId = self.treeView0.connect('row-activated',self.node0Selection)
      self.treeView1SignalId = self.treeView1.connect('row-activated',self.node1Selection)
      self.treeView2SignalId = self.treeView2.connect('row-activated',self.node2Selection)
      self.node2Signal = True
      self.firstRun = True

   def node0Selection(self, tree_view, path, column):
      try:
         self.treeView0.handler_block(self.treeView0SignalId)
         self.treeView1.handler_block(self.treeView1SignalId)
         self.treeView2.handler_block(self.treeView2SignalId)
         #import pdb; pdb.set_trace()
         self.logger.debug('Node2Signal: %s', str(self.node2Signal))
         if not self.node2Signal:
            self.node2Signal = not self.node2Signal

         row_num = tree_view.get_cursor()[0].get_indices()
         node = [x for x in self.node0List if x.title == tree_view.get_model()[row_num][0]][0]
         spider = Spider()
         if node.children is None:
            node = spider.buildNode(node.baseUrl, node.parent,1)

         if node.parent is None:
            self.node0List = [node]
            self.node0GridList.clear()
            self.node0GridList.append([node.title])

            self.node1List = node.children
            self.node1GridList.clear()
            [self.node1GridList.append([child.title]) for child in node.children]

            self.node2List = []
            self.node2GridList.clear()
         elif node.parent.parent is None:
            self.node0List = [node.parent]
            self.node0GridList.clear()
            self.node0GridList.append([node.parent.title])

            self.node1List = node.parent.children
            self.node1GridList.clear()
            [self.node1GridList.append([child.title]) for child in node.parent.children]

            self.node2List = node.children
            self.node2GridList.clear()
            [self.node2GridList.append([child.title]) for child in node.children]
         else:
            self.node0List = node.parent.parent.children
            self.node0GridList.clear()
            [self.node0GridList.append([child.title]) for child in node.parent.parent.children]
            self.node1List = node.parent.children
            self.node1GridList.clear()
            [self.node1GridList.append([child.title]) for child in node.parent.children]

            self.node2List = node.children
            self.node2GridList.clear()
            [self.node2GridList.append([child.title]) for child in node.children]

         self.renderWebKit(node.baseUrl)
         self.treeView0.set_cursor(row_num)
         self.treeView0.handler_unblock(self.treeView0SignalId)
         self.treeView1.handler_unblock(self.treeView1SignalId)
         self.treeView2.handler_unblock(self.treeView2SignalId)
      except Exception as e:
         import pdb; pdb.set_trace()
         self.logger.error(e)

   def node1Selection(self, tree_view, path, column):
      #import pdb; pdb.set_trace()
      self.treeView0.handler_block(self.treeView0SignalId)
      self.treeView1.handler_block(self.treeView1SignalId)
      self.treeView2.handler_block(self.treeView2SignalId)

      row_num = tree_view.get_cursor()[0].get_indices()
      node = [x for x in self.node1List if x.title == tree_view.get_model()[row_num][0]][0]
      spider = Spider()
      node = spider.buildNode(node.baseUrl, node.parent, 1)
      self.node2List = node.children
      self.node2GridList.clear()
      [self.node2GridList.append([child.title]) for child in node.children]
      self.renderWebKit(node.baseUrl)

      self.treeView1.set_cursor(row_num)
      self.treeView0.handler_unblock(self.treeView0SignalId)
      self.treeView1.handler_unblock(self.treeView1SignalId)
      self.treeView2.handler_unblock(self.treeView2SignalId)

   def node2Selection(self, tree_view, path, column):
      # For some reason only treeView2 is getting a second selection changed signal
      # While treeView1 is not.
      # To work around this while I debug the cause
      # We are eating every other signal
      self.logger.debug('Value of node2signal: ' + str(self.node2Signal))
      if not self.node2Signal:
         self.node2Signal = not self.node2Signal
         return

      if self.firstRun:
         self.firstRun = False
         self.node2Signal = not self.node2Signal

      self.treeView0.handler_block(self.treeView0SignalId)
      self.treeView1.handler_block(self.treeView1SignalId)
      self.treeView2.handler_block(self.treeView2SignalId)

      row_num = tree_view.get_cursor()[0].get_indices()
      node = [x for x in self.node2List if x.title == tree_view.get_model()[row_num][0]][0]
      self.logger.debug('Selected Node: ' + node.title)
      spider = Spider()

      if node.children is None:
         node = spider.buildNode(node.baseUrl, node.parent, 1)

      self.node0List = self.node1List
      self.node0GridList.clear()
      [self.node0GridList.append([child.title]) for child in self.node0List]

      self.node1List = self.node2List
      self.node1GridList.clear()
      [self.node1GridList.append([child.title]) for child in self.node1List]

      self.node2List = node.children
      self.node2GridList.clear()
      [self.node2GridList.append([child.title]) for child in self.node2List]

      self.treeView1.set_cursor(row_num)

      self.renderWebKit(node.baseUrl)
      
      self.treeView0.handler_unblock(self.treeView0SignalId)
      self.treeView1.handler_unblock(self.treeView1SignalId)
      self.treeView2.handler_unblock(self.treeView2SignalId)

   def renderWebKit(self, url):
      self.logger.debug('Rendering URL: ' + url)
      self.webView.load_uri(url)
      #import pdb; pdb.set_trace()
      self.show_all()

   def load_changed(self,webView, evt):
         if evt == WebKit2.LoadEvent.FINISHED:
            self.set_title(webView.get_title())
         else:
            self.set_title('Loading... {:0.1f}%'.format(webView.get_estimated_load_progress()))

   def load_failed(self,webView,evt, url, error):
      self.logger.error('Error loading url: %s - %s', url, error)

   def set_style(self, css):
         style_provider = Gtk.CssProvider()
         style_provider.load_from_data(css)
         Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            style_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
