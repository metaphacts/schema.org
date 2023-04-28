# metaphacts schema.org Ontology Transformer

## Description
We have created a transformer for the schema.org Ontology that creates an OWL ontology and the corresponding SHACL shapes. 
The transformer builds upon the existing schema.org python scripts. 

Our build script downloads the schema.org repository from git (https://github.com/schemaorg/schemaorg) and checks out the latest stable release (currently `tags/v15.0-release`).

### Heuristics
schema.org typically uses `rdf:Property` and additional `domainIncludes` or `rangeIncludes` to define attribute and relations for classes.
This can result in mixed property ranges (e.g., `schema:URL, schema:Text, schema:Thing`)

Our transformation script uses a heuristic to deal with such cases.
In this heuristic, we remove all datatype. In most cases the datatype is a string therefore the assignment to object properties with their ranges provides more semantic expressivity. 

Additionally, we provide a configuration file `config.json` 
This configuration file provides the means to overwrite the range for specified properties. 
```
"propertyMapper": {
    "https://schema.org/image":"http://www.w3.org/2001/XMLSchema#anyURI",
    "https://schema.org/logo":"http://www.w3.org/2001/XMLSchema#anyURI",
    "https://schema.org/photo":"http://www.w3.org/2001/XMLSchema#anyURI",
    "https://schema.org/jobTitle":"http://www.w3.org/2001/XMLSchema#string"
  },
```
The `propertyMapper` is an object that takes a list of tuples.
The first element it the schema property we want to overwrite.
The second element represents the range.
Please note that all other ranges will be removed. 

### Filtering
The configuration file provides additional means to filter only related classes and properties for specific use cases. 
We provide an example configuration file for the resourcehub use case `resourcehub-example-config.json`. 

Please not that the transformer takes the content of the `config.json` file for mappings and filtering. Additionally, these filtering mechanisms do not provide any reasoning on subclasses or the inherited properties form superclasses.

###  Shapes and Restrictions
We exclude `rdfs:domain` and `rdfs:range` form the generation.
Instead we provide SHACL shapes for the individual classes and their attributes and relations.


## Generated Ontologies
The transformation script provides three output files which are stored in the `ontologies` folder.
* schema-org.ttl
The full schema.org model including OWL declarations (for classes, relations and attributes) and SHACL Shapes. 
* schema-org-owl.ttl
Only OWL declarations of the schema.org model
* schema-org-shacl-shapes.ttl
Only SHACL shapes of the schema.org model


## How to use
* `./build.sh` 
  * Downloads the schema.org repository and switch to the lates stable release version based on the branch tag (currently `tags/v15.0-release`)
  * Please note: you might need to install additional python modules to execute the the transformer. The `schemaorg/software` has the `requirements.txt` file. Please switch to this folder and execute `pip3 install -r requirements.txt` if additional packages are required. 

* run `./clear.sh` to remove the `schemaorg` git repository from the file system
