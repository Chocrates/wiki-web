import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import math
import ctypes
from wikiNode import WikiNode
import cairo

class TreeWindow(Gtk.Window):
   def __init__(self, wikiNode):
      Gtk.Window.__init__(self, title='Wiki Tree - root name')
      self.node = wikiNode

      self.set_border_width(10)

#      self.resize(1280,768)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.connect('delete-event', Gtk.main_quit)

      box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
      self.add(box_outer)

#      listbox = Gtk.ListBox()
#      listbox.set_selection_mode(Gtk.SelectionMode.NONE)
#      box_outer.pack_start(listbox,True,True,0)
#
#      row = Gtk.ListBoxRow()
#      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=50)
#
#      row.add(hbox)
#
#      vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
#      hbox.pack_start(vbox,True,True,0)
#
#      label1 = Gtk.Label('Automatic Date & Time', xalign=0)
#      label2 = Gtk.Label('Requires internet access', xalign=0)
#
#      vbox.pack_start(label1, True, True,0)
#      vbox.pack_start(label2, True,True,0)
#      switch = Gtk.Switch()
#      switch.props.valign = Gtk.Align.CENTER
#      hbox.pack_start(switch,False,True,0)
#
#      listbox.add(row)
#
#      row = Gtk.ListBoxRow()
#      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=50)
#      row.add(hbox)
#
#      label = Gtk.Label('Enable Automatic Update', xalign=0)
#
#      check = Gtk.CheckButton()
#      hbox.pack_start(label, True,True,0)
#      hbox.pack_start(check,False,True,0)
#
#      listbox.add(row)
#
#      row = Gtk.ListBoxRow()
#      hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
#
#      row.add(hbox)
#
#      label = Gtk.Label('Date Format', xalign=0)
#      combo = Gtk.ComboBoxText()
#      combo.insert(0,'0','24-hour')
#      combo.insert(1,'1','AM/PM')
#      hbox.pack_start(label,True,True,0)
#      hbox.pack_start(combo,False,True,0)
#
#      listbox.add(row)
#
#      listbox_2 = Gtk.ListBox()
#
#      items = 'This is a sorted ListBox'.split()
#
#      for item in items:
#         listbox_2.add(ListBoxRowWithData(item))
#
#         def sort_func(row_1, row_2, data, notify_destroy):
#            return row_1.data.lower() > row_2.data.lower()
#
#         def filter_func(row,data,notify_destroy):
#            return False if row.data == 'Fail' else True
#
#         listbox_2.set_sort_func(sort_func,None,False)
#         listbox_2.set_filter_func(filter_func,None,False)
#
#         box_outer.pack_start(listbox_2,True,True,0)
#         listbox_2.show_all()
#
      listbox_3 = Gtk.ListBox()
      listbox_3.set_selection_mode(Gtk.SelectionMode.NONE)

      nodeRow = Gtk.ListBoxRow()
      listbox_3.add(nodeRow)

      nodeBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,spacing=10)
      nodeRow.add(nodeBox)

      rootBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
      rootButton = Gtk.Button(self.node.rawPageBody.title.string, xalign=0)
      rootBox.add(rootButton)
      nodeBox.add(rootBox)

      box_outer.pack_start(listbox_3,True,True,0)
      listbox_3.show_all()

      childBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=10)
      nodeBox.add(childBox)

      for child in self.node.children:
         childLabel = Gtk.Button(child.rawPageBody.title.string,xalign=0)
         childBox.add(childLabel)

#      drawArea = Gtk.DrawingArea()
#      drawArea.connect('draw',self.renderCairo)
#      self.add(drawArea)
      self.show_all()

   def renderCairo(self, widget, event):
      cr = self.get_window().cairo_create()
      cr.set_source_rgb(0.7,0.2,0.0)
      cr.select_font_face('ComicSans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
      cr.set_font_size(13)

      w = self.get_allocation().width
      h = self.get_allocation().height
#      cr.move_to((w-len(self.node.baseUrl)*4)/2,30)
#      cr.show_text(self.node.baseUrl)
      
      def draw_children(node, xLocation,depth):
#         import pdb; pdb.set_trace()
         cr.move_to(xLocation, depth)
         cr.show_text(node.rawPageBody.title.string)
         if not node.children is None:
            numChildren = len(node.children)
            for i in range(0,len(node.children)):
               draw_children(node.children[i], i * 250 , depth+15)

      draw_children(self.node, 20,20)

class ListBoxRowWithData(Gtk.ListBoxRow):
   def __init__(self,data):
      super(Gtk.ListBoxRow,self).__init__()
      self.data = data
      self.add(Gtk.Label(data))
