#!/usr/bin/env python
# encoding: utf-8

from sdoConstants import *

class OwlProperty():
  def __init__(self, uri):
    self.propType='owl:ObjectProperty'
    self.label= None
    self.comment= None
    self.domains = []
    self.ranges = []
    self.subProperties = [] 
    self.uri=uri
    self.isMixed=False

  def setType(self,type):
    self.propType=type

  def applyHeuristics(self):
    while self.isMixed==True:
      for dataRange in self.ranges:
        if (dataRange in MAPPED_DATATYPES):
          self.ranges.remove(dataRange)
      self.checkForMultipleTypes()
      #select one of the ranges;

  

  def isPureObjectProp(self,ranges):
    for r in ranges:
      if r in MAPPED_DATATYPES:
         return False
    return True

  def checkForMultipleTypes(self):
     self.isMixed=False
     if len(self.ranges) > 0 : 
      for range in self.ranges: 
        if self.propType=='owl:ObjectProperty':
          #note here ranges could have also datatypes;
          pureObjectProp = self.isPureObjectProp(self.ranges)
          if not pureObjectProp:
            self.isMixed=True

  def getPropDef(self):
    propDef="<%s> rdf:type %s" %(self.uri, self.propType)

    if self.label : 
      propDef+=";\n\t rdfs:label \"%s\"@en" % (self.label)
    if self.comment : 
      propDef+=";\n\t rdfs:comment \"\"\" %s \"\"\"@en" % (self.comment)

    #extract sub properties 
    if len(self.subProperties) > 0 : 
      propDef+=";\n\t rdfs:subPropertyOf "
      for sub in self.subProperties: 
        propDef+="<%s>, " % (sub)
      propDef = propDef[:-2]

    
    propDef+=".\n\n"
    return propDef

