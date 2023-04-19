#!/usr/bin/env python
# encoding: utf-8

class ShapeNode():
  def __init__(self):
    self.propType='sh:NodeShape'
    self.targetClass=None
    self.property=None
    self.objectProperty=None
    self.representation=''
    self.rangeClass=[]
  
  def buildNodeShape(self):
    self.representation+='[] a %s; \n' %(self.propType)
    self.representation+='  sh:targetClass <%s>; \n' %(self.targetClass)
    self.representation+='  sh:property '
    for range in self.rangeClass: 
      self.representation+='[ a sh:PropertyShape; \n'
      self.representation+='    sh:path <%s>;\n' %(self.property)
      if self.objectProperty == True:
        self.representation+='    sh:class <%s>\n' %(range)
      else:
        self.representation+='    sh:datatype <%s>\n' %(range)
      self.representation+='  ], '
    #remove the last two chars and close the statement. 
    self.representation = self.representation[:-2]+' .\n\n'

  def getShapeDef(self):
    return self.representation
