#!/usr/bin/env python
# encoding: utf-8


from sdoConstants import *
from OwlProperty import *
from OwlClass import *
from ShaclShape import *


class SdoTtlTransformer():

  def __init__(self, config):
    self.config=config 
    self.typesCount = self.propsCount = self.namedCount = 0
    self.classes = [] 
    self.properties = []
    self.mixedProps=[]
    self.shapes=[]
    self.numMixedProperties = 0
    self.numAllProperties = 0
    self.propertyMapper=config.get('propertyMapper')
    self.filteredClasses=config.get('filteredClasses')
    self.filteredProperties=config.get('filteredProperties')

   
    

    self.createStaticInformation()
    self.loadGraph()
    # print("Number of mixed Properties", self.numMixedProperties, "/", len(self.properties))
    # for x in self.mixedProps:
    #   print(str(x.uri), x.ranges)

  def mapPropertyByConfig(self,prop, object):
    if self.propertyMapper:
      mapped=self.propertyMapper.get(str(prop))
      if mapped:
        return mapped
      
    return object

  def mapPropertyToXsd(self,prop):
    if prop=='https://schema.org/Boolean':
      return 'http://www.w3.org/2001/XMLSchema#boolean'
    if prop=='https://schema.org/Date':
      return 'http://www.w3.org/2001/XMLSchema#date'
    if prop=='https://schema.org/DateTime':
      return 'http://www.w3.org/2001/XMLSchema#dateTime'
    if prop=='https://schema.org/Number':
      return 'http://www.w3.org/2001/XMLSchema#number'
    if prop=='https://schema.org/Float':
      return 'http://www.w3.org/2001/XMLSchema#float'
    if prop=='https://schema.org/Integer':
      return 'http://www.w3.org/2001/XMLSchema#integer'
    if prop=='https://schema.org/Time':
      return 'http://www.w3.org/2001/XMLSchema#time'
    if prop=='https://schema.org/Text':
      return 'http://www.w3.org/2001/XMLSchema#string'
    if prop=='https://schema.org/URL':
      return 'http://www.w3.org/2001/XMLSchema#anyURI'
    return prop

  def loadGraph(self):
    self.list(SdoTermSource.sourceGraph())

  def list(self,graph):
    types = {}
    props = {}
    

    # CLASSES
    for (s,p,o) in graph.triples((None,RDF.type,RDFS.Class)):
      if s.startswith("https://schema.org"):
        types.update({s:graph.identifier})

    for t in sorted(types.keys()):
      self.outputType(t,graph)

    # PROPERTIES
    for (s,p,o) in graph.triples((None,RDF.type,RDF.Property)):
      if s.startswith("https://schema.org"):
        props.update({s:graph.identifier})
    
    for p in sorted(props.keys()):
      self.properties.append(self.outputProp(p,graph))


    # SHAPES
    for p in self.properties:
      self.outputShape(p)



  def outputType(self, uri, graph):
        str_uri=str(uri)
        if str_uri == "https://schema.org/Boolean" or str_uri == "https://schema.org/Text":
          return
        if str_uri == "https://schema.org/Number" or str_uri == "https://schema.org/Date":
          return
        if str_uri == "https://schema.org/Time" or str_uri == "https://schema.org/DateTime":
          return
        if str_uri == "https://schema.org/DataType":
          return
        if str_uri == "https://schema.org/Float":
          return
        if str_uri == "https://schema.org/Integer":
          return  
        if str_uri == "https://schema.org/CssSelectorType":
          return
        if str_uri == "https://schema.org/PronounceableText":
          return      
        if str_uri == "https://schema.org/URL":
          return   
        if str_uri == "https://schema.org/XPathType":
          return

        self.typesCount += 1

        owlClass=OwlClass(uri)
        name=str_uri.split("/")[-1]
        owlClass.name=name

        cls="<%s> rdf:type owl:Class" %(uri)
        
                
        for (p,o) in graph.predicate_objects(uri):
            if p == RDFS.label:
                cls += ";\n\t rdfs:label \"%s\"@en" %(o)
                owlClass.label=o
            elif p == RDFS.comment:
                cls += ";\n\t rdfs:comment \"\"\" %s \"\"\"@en" % (o)
                owlClass.comment=o
            elif p == RDFS.subClassOf:
               cls += ";\n\t rdfs:subClassOf <%s>" % (o)
               owlClass.subClasses.append(o)
# >> TODO: Currently removed from extraction script
###################################
#           elif p == URIRef(VOCABURI + "isPartOf"): #Defined in an extension
#               ext = str(o)
#           elif p == RDF.type and o == URIRef(VOCABURI + "DataType"): #A datatype
#               s = SubElement(typ,"rdfs:subClassOf")
#               s.set("rdf:resource",VOCABURI + "DataType")
#################################
        cls += ".\n\n" #closing the class description;
        owlClass.representation=cls;
        self.classes.append(owlClass)
      #  typ.append(self.addDefined(uri,ext))


  def outputProp(self,uri,graph):
    self.propsCount += 1
    
    datatypeonly = True

    schemaProperty = OwlProperty(uri)

    for (p,o) in graph.predicate_objects(uri):
     
      if p == RDFS.label:
        schemaProperty.label = o
      elif p == RDFS.comment:
        schemaProperty.comment= o
      elif p == RDFS.subPropertyOf:
         schemaProperty.subProperties.append(o)
      elif p == RANGEINC:
        mappedObject=self.mapPropertyByConfig(uri, str(o))
        mapped=self.mapPropertyToXsd(mappedObject)
        if mapped not in schemaProperty.ranges:
          schemaProperty.ranges.append(mapped)
        if mapped not in MAPPED_DATATYPES:
          datatypeonly = False
      elif p == DOMAININC:
        schemaProperty.domains.append(str(o))

    if datatypeonly == True:
      schemaProperty.setType('owl:DatatypeProperty')
    schemaProperty.checkForMultipleTypes()
    if schemaProperty.isMixed == True:
      # removed all datatypeProps 
      filtered=schemaProperty.ranges
      needsIteration=True

      while needsIteration:
        needsIteration=False
        for f in filtered:
          if (f in MAPPED_DATATYPES):
            filtered.remove(f)
            needsIteration=True
      self.mixedProps.append(schemaProperty)
      self.numMixedProperties+=1
    return schemaProperty
  
  def outputShape(self,prop):
    #self.shapes.append(ShaclShape(prop))
    x=ShaclShape(prop)
    self.shapes.append(x)



  def createStaticInformation(self):
    self.disclaimer = """########
# Generated from Schema.org version: %s released: %s
# Using Metaphacts transformation script.
# @Author: Vitalis Wiens
######## 
""" % (getVersion(),getVersionDate(getVersion()))
    
    self.prefixDef=''
    for (k,v) in NAMESPACES.items():
          self.prefixDef+='@prefix %s: <%s> .\n' % (k,v)


    self.ontologyDef="""
<%s> a owl:Ontology;
    owl:versionInfo \"%s\";
    dcterms:modified \"%s\";
    rdfs:label "Schema.org Ontology";
    dcterms:title "Schema.org Ontology";
    rdfs:description "Schema.org Vocabulary transformed to OWL";
    dcterms:description "Schema.org Vocabulary transformed to OWL". \n
""" % (VOCABURI, getVersion(),getVersionDate(getVersion()))
    
  def show(self):
    print("Created OWL TTL representation")
    print(self.disclaimer)
    print(self.prefixDef)
    print(self.ontologyDef)
    print(self.classes)
    print(self.shapes)

  def filterClasses(self):
    existingClasses=self.classes
    filteringArray=self.filteredClasses
    filteredResult=[]
    for item in filteringArray:
      for existingClass in existingClasses:
        stringUri=str(existingClass.uri)
        if stringUri == item:
          filteredResult.append(existingClass)
    self.classes=filteredResult

  def filterPropertiesAndShapes(self):
    existingProps=self.properties
    existingShapes=self.shapes
    filteringArray=self.filteredProperties
    filteredResultProps=[]
    filteredResultShapes=[]
    for item in filteringArray:
      for existingProp in existingProps:
        stringUri=str(existingProp.uri)
        if stringUri == item:
          if existingProp not in filteredResultProps:
            filteredResultProps.append(existingProp)

      for existingShape in existingShapes:
        stringUri=str(existingShape.prop.uri)
        if stringUri == item:
          #check if domains are applicable
          existingShape.filterByExistingDomains(self.classes)
          if existingShape not in filteredResultShapes:
            filteredResultShapes.append(existingShape)

    self.properties=filteredResultProps
    self.shapes=filteredResultShapes

  def applyFilters(self):
     #apply filters
    if self.filteredProperties !=None or self.filteredClasses !=None:
      
      if len(self.filteredClasses)==0:
        print("No Classes filtered")
      else:
        self.filterClasses()
      if len(self.filteredProperties)==0:
        print("No Properties filtered")
      else:
        self.filterPropertiesAndShapes()


  def writeOwl(self, filename):
    self.applyFilters()

    f = open(filename,"w")
    f.write(self.disclaimer)
    f.write(self.prefixDef)
    f.write(self.ontologyDef)
    f.write("######################################### \n")
    f.write("#\t\t\t Class Definitions  \n")
    f.write("######################################### \n\n")
    for x in self.classes:
      f.write(x.getRepresentation())

    f.write("######################################### \n")
    f.write("#\t\t\t ObjectProperty Definitions  \n")
    f.write("######################################### \n\n")
    
    for x in self.properties:
      if x.propType == 'owl:ObjectProperty':
        f.write(x.getPropDef())

    f.write("######################################### \n")
    f.write("#\t\t\t DatatypeProperty Definitions \n")
    f.write("######################################### \n\n")
    for x in self.properties:
      if x.propType == 'owl:DatatypeProperty':
        f.write(x.getPropDef())

  def writeShapes(self, filename):
    self.applyFilters()
    f = open(filename,"w")
    f.write("######################################### \n")
    f.write("#\t\t\t Schema.Org SHACL shape Definitions  \n")
    f.write("######################################### \n\n")
    for x in self.shapes:
      if x:
        f.write(x.getShapeDef())

    f.close()


   
  def write(self,filename):
    self.applyFilters()
    f = open(filename,"w")
    f.write(self.disclaimer)
    f.write(self.prefixDef)
    f.write(self.ontologyDef)
    f.write("######################################### \n")
    f.write("#\t\t\t Class Definitions  \n")
    f.write("######################################### \n\n")
    for x in self.classes:
      f.write(x.getRepresentation())

    f.write("######################################### \n")
    f.write("#\t\t\t ObjectProperty Definitions  \n")
    f.write("######################################### \n\n")
    
    for x in self.properties:
      if x.propType == 'owl:ObjectProperty':
        f.write(x.getPropDef())

    f.write("######################################### \n")
    f.write("#\t\t\t DatatypeProperty Definitions \n")
    f.write("######################################### \n\n")
    for x in self.properties:
      if x.propType == 'owl:DatatypeProperty':
        f.write(x.getPropDef())

    f.write("######################################### \n")
    f.write("#\t\t\t SHACL shape Definitions  \n")
    f.write("######################################### \n\n")
    for x in self.shapes:
      if x:
        f.write(x.getShapeDef())
    
    f.close()
