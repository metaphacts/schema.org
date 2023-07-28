#!/bin/bash

#check if schemaorg directory exits 
DIR="./schemaorg"
if [ -d "$DIR" ]; then
  # Take action if $DIR exists. #
  echo "Removing ${DIR}"
  rm -rdf ${DIR}
fi