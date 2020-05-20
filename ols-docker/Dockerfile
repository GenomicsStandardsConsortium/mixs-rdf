FROM simonjupp/ebi-ols:3.1.1

ENV OLS_HOME /opt/ols
ENV JAVA_OPTS "-Xmx1g"
ENV SOLR_VERSION 5.5.3

# ADD *.owl ${OLS_HOME}

# For a single ontology file, you don't put the '/' after ${OLS_HOME}
ADD mixs_package_class.owl ${OLS_HOME}/
ADD mixs_package_dp.owl ${OLS_HOME}/

ADD ols-config.yaml ${OLS_HOME}

## Start MongoDB
### Load configuration into MongoDB
RUN mongod --smallfiles --fork  --logpath /var/log/mongodb.log \
    && cd ${OLS_HOME} \ 
    && java -Dols.obofoundry.ontology.config=foo.yaml -Dols.ontology.config=file://${OLS_HOME}/ols-config.yaml -jar ${OLS_HOME}/ols-config-importer.jar \
    && sleep 10

## Start MongoDB and SOLR
## Build/update the indexes
RUN mongod --smallfiles --fork --logpath /var/log/mongodb.log \
  && /opt/solr-${SOLR_VERSION}/bin/solr -Dsolr.solr.home=${OLS_HOME}/solr-5-config/ -Dsolr.data.dir=${OLS_HOME} \
  && java ${JAVA_OPTS} -Dols.home=${OLS_DATA} -jar ${OLS_HOME}/ols-indexer.jar  

## Expose the tomcat port 
EXPOSE 8080

CMD cd ${OLS_HOME} \
    && mongod --smallfiles --fork --logpath /var/log/mongodb.log \
    && /opt/solr-${SOLR_VERSION}/bin/solr -Dsolr.solr.home=${OLS_HOME}/solr-5-config/ -Dsolr.data.dir=${OLS_HOME} \
    && java -jar -Dols.home=${OLS_HOME} ols-boot.war

