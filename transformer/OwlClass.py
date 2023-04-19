#!/usr/bin/env python
# encoding: utf-8

from sdoConstants import *

class OwlClass():
  def __init__(self, uri):
    self.propType='owl:Class'
    self.label = None
    self.comment = None
    self.subClasses = [] 
    self.uri = uri
    self.name=None
    self.representation = None

  def getRepresentation(self):
    return self.representation