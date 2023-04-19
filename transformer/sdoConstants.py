#!/usr/bin/env python
# encoding: utf-8

import sys
import os

os.chdir("schemaorg")
for path in [os.getcwd(),"software/util","software/SchemaTerms","software/SchemaExamples"]:
  sys.path.insert( 1, path ) #Pickup libs from local directories
  


from sdotermsource import SdoTermSource 
from software.util.schemaversion import getVersion, getVersionDate
import rdflib
from rdflib import Graph
from rdflib.term import URIRef, Literal
from rdflib.parser import Parser
from rdflib.serializer import Serializer
from rdflib.plugins.sparql import prepareQuery
from rdflib.compare import graph_diff
from rdflib.namespace import RDFS, RDF

from xml.etree import ElementTree as ET
from xml.dom import minidom
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

from buildsite import *
from sdotermsource import SdoTermSource 
from sdoterm import *
from localmarkdown import Markdown



VOCABURI = SdoTermSource.vocabUri()

NAMESPACES = {
    "base"   : VOCABURI,
    "schema" : VOCABURI,
    "shape"  : "https://schema.org/shacl-shapes/",
    "sh"     : "http://www.w3.org/ns/shacl#",
    "rdf"    : "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs"   : "http://www.w3.org/2000/01/rdf-schema#",
    "owl"    : "http://www.w3.org/2002/07/owl#",
    "dcterms": "http://purl.org/dc/terms/",
    "xsd"    : "http://www.w3.org/2001/XMLSchema#"
}

DOMAININC = URIRef(VOCABURI + "domainIncludes")
RANGEINC = URIRef(VOCABURI + "rangeIncludes")
INVERSEOF = URIRef(VOCABURI + "inverseOf")
SUPERSEDEDBY = URIRef(VOCABURI + "supersededBy")
DEFAULTRANGES = [VOCABURI + "Text",VOCABURI + "URL",VOCABURI + "Role"]
DATATYPES = [VOCABURI + "Boolean",
            VOCABURI + "Date",
            VOCABURI + "DateTime",
            VOCABURI + "Text",
            VOCABURI + "URL",
            VOCABURI + "Number",
            VOCABURI + "Float",
            VOCABURI + "Integer",
            VOCABURI + "Time"]

MAPPED_DATATYPES = ['http://www.w3.org/2001/XMLSchema#boolean',
       'http://www.w3.org/2001/XMLSchema#date',
       'http://www.w3.org/2001/XMLSchema#dateTime',
       'http://www.w3.org/2001/XMLSchema#number',
       'http://www.w3.org/2001/XMLSchema#float',
       'http://www.w3.org/2001/XMLSchema#integer',
       'http://www.w3.org/2001/XMLSchema#time',
       'http://www.w3.org/2001/XMLSchema#string',
       'http://www.w3.org/2001/XMLSchema#anyURI']

