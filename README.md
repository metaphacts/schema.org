# metaphacts schema.org ontology transformer

## Description
This transformer downloads the schema.org repository from git (https://github.com/schemaorg/schemaorg) and provides extensions that are build ontop to create the turtle representation of schema.org with SHACL shapes.

As schema.org typically uses `rdf:Property` and additional `domainIncludes` or `rangeIncludes` to define attribute and relations for classes, which may result in mixed property ranges (e.g., `schema:URL, schema:Text, schema:Thing`)

Our transformation script uses in such cases prefers the semantic expressive case, by removing datatypes form mixed types. 


Additionally, we provide a `config.json` in the transformer folder that offers the means to overwrite specific range types. 

Futhermore, we exclude `rdfs:domain` and `rdfs:range` form the generation and provide SHACL shapes instead for the individual classes and their attributes and relations.

## How to use
run `./build.sh` script that will download the necessary files, and switch to the lates stable release version based on the branch tag (currently `tags/v15.0-release`)
The generated ontology is saved in `ontologies/schema-org.ttl`

run `./clear.sh` to remove the `schemaorg` git repository from the file system


