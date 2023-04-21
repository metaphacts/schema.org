#!/usr/bin/env python
# encoding: utf-8

from ShapeNode import *

class ShaclShape():
  def __init__(self,prop):
    self.representation=None
    self.prop=prop
    self.nodeShapes=[]
    self.buildShapes(prop)
    
  def filterByExistingDomains(self, classesArray):
    # check if the nodeShape is okay
    applicableNodeShapes=[]
    
    for nShape in self.nodeShapes:
      targetClass=nShape.targetClass
      available=list(filter(lambda i: str(i.uri)==targetClass, classesArray) )
      if len(available)>0:
        applicableNodeShapes.append(nShape)
   
    self.buildShapeByNodes(applicableNodeShapes, self.prop)

  def buildShapeByNodes(self,nodes,prop):
    self.representation="# -- %s --\n" % (str(prop.uri))
    for nodeShape in nodes:
      self.representation+=nodeShape.representation
  
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
      self.nodeShapes.append(nodeShape)
      self.representation+=nodeShape.representation
  
  def getShapeDef(self):
    return self.representation