#!/usr/bin/python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import math

class TreeWindow(Gtk.Window):
   def __init__(self):
      Gtk.Window.__init__(self, title='Wiki Tree - root name')
      self.resize(640,480)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.connect('delete-event', Gtk.main_quit)

      darea = Gtk.DrawingArea()
      darea.connect('draw',self.expose)
      self.add(darea)

      self.show_all()

   def expose(self, widget,event):
#      cr = widget.get_property('window').cario_create()
      cr = self.get_window().cairo_create()
      cr.set_source_rgb(0.7,0.2,0.0)

      w = self.get_allocation().width
      h = self.get_allocation().height

      cr.translate(w/2,h/2)
      cr.arc(0,0,50,0,2*math.pi)
      cr.stroke_preserve()

      cr.set_source_rgb(0.3,0.4,0.6)
      cr.fill()

TreeWindow()
Gtk.main()
