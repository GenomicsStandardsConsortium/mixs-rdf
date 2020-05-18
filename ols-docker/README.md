# Running the EMBL-EBI Ontology Lookup Service with Docker  

To run the MIxS RDF files in a local [EBI's Ontology Lookup Service](https://www.ebi.ac.uk/ols/) web portal:
1. Build the Docker image by either using the shell script `docker-build.sh`, or executing the command `docker build -t mixs-rdf .`.
2. Start the Docker container by either using the shell script `docker-run.sh`, or executing the command `docker run -dtp 8080:8080 --rm --name mixs-rdf mixs-rdf`.
3. Access the OLS through your browser on http://localhost:8080.
4. After you are finished browsing, you stop the container by either using the shell script `docker-stop.sh`, or executing the command `docker container stop mixs-rdf`.

### NB: The data properties version of MIxS terms does not display correctly in ols-docker. A ticket has been been submitted regarding ols-docker and data properties.  


## Configuration 

To change the behavior of the ols-docker, edit [ols-config.yaml](ols-config.yaml) with the metadata for each ontology you want to load into OLS. Any ontology in OBO or OWL format will work. 

Note, to load an ontology from a local file on disk, you add the ontology to the `${OLS_HOME}` in the [Docker file](Dockerfile), directory and set `ontology_purl: file:///opt/ols/<filename>.owl` in the [ols-config.yaml file ](ols-config.yaml). Alternately you can use a URL to load an ontology from the web e.g. `ontology_purl: http://purl.obolibrary.org/obo/envo.owl` 

## Rebuilding the image and relaunching the container

After changing the configuration, you will need to rebuild the image and relaunch the container.  

First, make sure the container has stopped running by either using the shell script `docker-stop.sh`, or executing the command `docker container stop mixs-rdf`.

Second, rebuild the image by either using the shell script `docker-build.sh`, or executing the command `docker build -t mixs-rdf .`.  

Often, you may find it necessary to delete the image and container before rebuilding. This can be done by either using the shell script `docker-remove.sh`, or exeuting the commands` docker container rm mixs-rdf` and `docker image rm mixs-rdf`

Finally, relaunch the by container by either using the shell script `docker-run.sh`, or executing the command `docker run -dtp 8080:8080 --rm --name mixs-rdf mixs-rdf`.
