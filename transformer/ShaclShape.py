#!/usr/bin/env python
# encoding: utf-8

from ShapeNode import *

class ShaclShape():
  def __init__(self,prop):
    self.representation=None
    self.buildShapes(prop)
  
  def buildShapes(self,prop):
    self.representation="# -- %s --\n" % (str(prop.uri))
    for n in prop.domains:
      nodeShape=ShapeNode()
      nodeShape.property=str(prop.uri)
      nodeShape.targetClass=n
      if prop.propType == 'owl:ObjectProperty':
        nodeShape.objectProperty=True
      else:
        nodeShape.objectProperty=False
      nodeShape.rangeClass=prop.ranges
      nodeShape.buildNodeShape()
      self.representation+=nodeShape.representation
  
  def getShapeDef(self):
    return self.representation