#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#this import takes care of creating the constants and loads all required libs

from sdoConstants import *
from SdoTtlTransformationScript import *
import json

# Opening JSON file
f = open('../transformation-script/config.json')
# returns JSON object as
# a dictionary
config = json.load(f)

def main():
  print("Building", VOCABURI)
  transformationScript=SdoTtlTransformationScript(config)
  transformationScript.write('../ontologies/schema-org.ttl')
  transformationScript.writeShapes('../ontologies/schema-org-shacl-shapes.ttl')
  transformationScript.writeOwl('../ontologies/schema-org-owl.ttl')
  print("Done...\nGenerated files are stored in `ontologies` folder")
if __name__ == "__main__":
  if not (sys.version_info.major == 3 and sys.version_info.minor > 5):
      print("Python version %s.%s not supported version 3.6 or above required - exiting" % (sys.version_info.major,sys.version_info.minor))
      sys.exit(1)
  main()
