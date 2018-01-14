#!/usr/bin/python3
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
import math
from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import ctypes
from wikiNode import WikiNode
import cairo

# Fragment Shader, static red color
FRAGMENT_SOURCE = '''
#version 330
uniform vec4 textColor;
uniform sampler2D textureUnit;

#if __VERSION__ >= 130
in vec4 texCoord;
out vec4 gl_FragColor;
#else
varyingvec4 texCoord;
#endif

void main(){
   vec4 red = texture(textureUnit, texCoord.st);
   gl_FragColor = vec4(1.0,1.0,1.0, red.r) * textColor;
}'''

# Vertex Shader, passthrough
VERTEX_SOURCE = '''
#version 330
uniform mat4 projMatrix;
uniform mat4 modelViewMatrix;
// vertex pos
in vec4 pos;
// text coord
in vec2 itexCoord;
out vec4 otexCoord;

void main(){
otexCoord = vec4(itexCoord.s, itexCoord.t, 0.0, 1.0);
gl_Position = projMatrix * modelViewMatrix * vec4(pos.x, pos.y, 0.0,1.0);
}'''


class TreeWindow(Gtk.Window):
   def __init__(self, wikiNode):
      Gtk.Window.__init__(self, title='Wiki Tree - root name')
      self.node = wikiNode
      self.resize(1280,768)
      self.set_position(Gtk.WindowPosition.CENTER)
      self.connect('delete-event', Gtk.main_quit)

      #darea = Gtk.GLArea()
      #darea.set_has_depth_buffer(False)
      #darea.set_has_stencil_buffer(False)
      #darea.connect('render',self.render)

      #self.add(darea)

      drawArea = Gtk.DrawingArea()
      drawArea.connect('draw',self.renderCairo)
      self.add(drawArea)
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





      def render(self, area,ctx):
         ctx.make_current()

         glClearColor(1,1,1,1)
         glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
         VERTEX_SHADER_PROG = shaders.compileShader(VERTEX_SOURCE, GL_VERTEX_SHADER)
         FRAGMENT_SHADER_PROG = shaders.compileShader(FRAGMENT_SOURCE, GL_FRAGMENT_SHADER)

         self.shader_prog = shaders.compileProgram(VERTEX_SHADER_PROG, FRAGMENT_SHADER_PROG)
         self.make_triangle()

      def make_triangle(self):
         vob = glGenVertexArrays(1)
         glBindVertexArray(vob)

         vb = glGenBuffers(1)
         glBindBuffer(GL_ARRAY_BUFFER, vb)

         pos = glGetAttribLocation(self.shader_prog, 'pos')
         glEnableVertexAttribArray(pos)

         glVertexAttribPointer(pos,3,GL_FLOAT,False, 0, ctypes.c_void_p(0))

         vertices = np.array([-0.6, -0.6,0.0,
                           0.0,0.6,0.0,
                           0.6,-0.6,0.0,
                           0.9,-0.1,0.0
                           ], dtype=np.float32)
         glBufferData(GL_ARRAY_BUFFER, 96, vertices, GL_STATIC_DRAW)
         glBindVertexArray(0)
         glDisableVertexAttribArray(pos)
         glBindBuffer(GL_ARRAY_BUFFER,0)
         self.display(vob)

   def display(self, vert):
      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
      glUseProgram(self.shader_prog)
      glBindVertexArray(vert)
      glDrawArrays(GL_TRIANGLES, 0, 3)
      glDrawArrays(GL_TRIANGLES, 4, 3)
      glBindVertexArray(0)
      glUseProgram(0)
