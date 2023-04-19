#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#this import takes care of creating the constants and loads all required libs

from sdoConstants import *
from SdoTtlTransformer import *
import json

# Opening JSON file
f = open('../transformer/config.json')
# returns JSON object as
# a dictionary
config = json.load(f)

def main():
  print("Building", VOCABURI)
  print(config)
  transformer=SdoTtlTransformer(config)
  transformer.write('../ontologies/schema-org.ttl')
  
if __name__ == "__main__":
  if not (sys.version_info.major == 3 and sys.version_info.minor > 5):
      print("Python version %s.%s not supported version 3.6 or above required - exiting" % (sys.version_info.major,sys.version_info.minor))
      sys.exit(1)
  main()
