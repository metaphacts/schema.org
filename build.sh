#!/bin/bash

#check if schemaorg directory exits 
DIR="./schemaorg"
if [ -d "$DIR" ]; then
  # Take action if $DIR exists. #
  echo "Schema directory exists"
else 
  echo "Cloning schema.org form github into ${DIR} ..."
  git clone git@github.com:schemaorg/schemaorg.git ${DIR} 
  cd ${DIR}
  # checkout the latest stable tag which has the proper versions in 
  # the file versions.json and create new branch for that
  git checkout -b metaphacts-schema-org-transformer tags/v15.0-release  
  cd ..
fi
python3 ./transformer/transformer.py
