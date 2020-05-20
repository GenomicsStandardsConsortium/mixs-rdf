import os, sys
import pandas as pds
from rdflib import Graph, URIRef, OWL, RDF, RDFS, Literal, BNode, Namespace
from rdflib.namespace import RDFS, DCTERMS, NamespaceManager



def mixs_sheet_df_to_rdf (
        sheet_df,
        mixs_version,
        package_name,
        file_name,
        term_type='class',
        base_iri='https://gensc.org/mixs#',
        ontology_iri='https://gensc.org/mixs.owl',
        ontology_format='turtle'):
    """ 
    Builds an ontology (rdflib graph) from a dataframe created from a MIxS sheet.
    Within the module, it is called by the mixs_package_file_to_rdf function in order to convert a 
    specific MIxS Excel sheet to rdf. It may also be used transale a csv or tsv.
    
    Args:
        sheet_df: The dataframe containing data from a spefice sheet.
        mixs_version: The version of MIxS package.
        package_name: The MIxS package name under which the terms will be grouped.
        file_name: The name of MIxS package file.
        term_type: Specifies if the MIxS terms will be represented as classes or data properties.
                   Accepted values: 'class', 'data property'
                   Default: 'class'
        file_type: The type of file being processed. 
                   If file type is not 'excel', a field separator/delimitor must be provided.
                   Default: 'excel'
        base_iri: The IRI used as prefix for MIxS terms.
        ontology_iri: The IRI used for the output ontology.
        ontology_format: The rdf syntax of the output ontology.
                   Accepted values: 'turtle', 'ttl', 'nt', 'ntriples', 'trix', 'json-ld', 'xml'
                   Default: 'turtle'
    Returns:
        rdflib Graph
    """
        
    def _make_annotation_properties (graph):
        """
        Inner function for adding annaotiaon properties to graph.
        """
        
        ## add mixs version annaotiaon property
        graph.add( (mixs.mixs_version, RDF.type, OWL.AnnotationProperty) )
        graph.add( (mixs.mixs_version, RDFS.label, Literal('MIxS version')) )

        ## add mixs file name annotation property
        graph.add( (mixs.mixs_file_name, RDF.type, OWL.AnnotationProperty) )
        graph.add( (mixs.mixs_file_name, RDFS.label, Literal('MIxS file name')) )
        
        ## column name iris as annaotiaon properties
        for col_name in col_names_dict.keys():
            pred_iri = col_name_iris_dict[col_name]
            label = Literal(col_names_dict[col_name])
        
            graph.add( (pred_iri, RDF.type, OWL.AnnotationProperty) )
            graph.add( (pred_iri, RDFS.label, label) )
            
            return graph

    def _make_top_level_iris(graph):
        """
        Inner function for creating iris for top leve classes/properties and adding iris to graph.
        """
        ## add top level iri for mixs tersms
        #top_term_iri = mixs[f'mixs_term_version_{mixs_version}']
        top_term_iri = mixs.mixs_term
        top_term_label = Literal('MIxS term')

        graph.add( (top_term_iri, RDF.type, owl_type) )
        graph.add( (top_term_iri, RDFS.label, top_term_label) )
        
        ## add top level iri for terms packages
        #top_package_iri = mixs[f'mixs_term_version_{mixs_version}']
        #top_package_label = Literal(f'MIxS version {mixs_version}')

        top_package_iri = mixs.mixs_environmental_package
        top_package_label = Literal(f'MIxS environmental package')
        
        graph.add( (top_package_iri, RDF.type, owl_type) )
        graph.add( (top_package_iri, RDFS.label, top_package_label) )

        return (top_term_iri, top_package_iri)

        
    def _make_pakage_iri(graph):
        """
        Inner funciton for creating and adding package iri to graph.
        """
        package_iri_str = \
            package_name.replace(' - ', '-').replace(' ', '') + f'_v{mixs_version}'
        
        package_iri = mixs[package_iri_str]
        package_label = Literal(f'{package_name} version {mixs_version}')
    
        graph.add( (package_iri, RDF.type, owl_type) )
        graph.add( (package_iri, RDFS.label, package_label) )
        graph.add( (package_iri, sub_relation, top_package_iri) )
        graph.add ( (package_iri, mixs.mixs_version, Literal(mixs_version)) )
        graph.add ( (package_iri, mixs.mixs_file_name, Literal(os.path.basename(file_name))) )

        return package_iri



    def _make_triples (graph, sheet_df):
        """
        Inner function for adding triples to graph.
        """        
        ## add rows in sheet to graph
        for row in sheet_df.itertuples(index=False): # note: ignore index value
            ## add mixs term
            mixs_term_iri = mixs[row.structured_comment_name.strip()]
            label = Literal(row.item)
            version = Literal(mixs_version)

            ## add term to graph
            graph.add( (mixs_term_iri, RDF.type, owl_type) )
            graph.add( (mixs_term_iri, RDFS.label, label) )
            graph.add( (mixs_term_iri, mixs.mixs_version, version) )

            ## specify term parents
            graph.add( (mixs_term_iri, sub_relation, package_iri) )
            graph.add( (mixs_term_iri, sub_relation, top_term_iri) )
            
            ## add mixs term triples to graph using column name iris
            for col_name in col_names_dict.keys():
                pred_iri = col_name_iris_dict[col_name]
                obj = Literal(getattr(row, col_name))
            
                graph.add( (mixs_term_iri, pred_iri, obj) )
            #break # used for testing
                
        return graph
    
    ## lowercase column names so that they are easier to work with
    col_labels = [col.lower().strip() for col in sheet_df.columns]

    ## map col names to labesl and update dataframe columns
    col_names_dict = \
        { col_label.replace(' ', '_') : col_label for col_label in col_labels }
    sheet_df.columns = col_names_dict.keys()
        
    ## map remaining column names iris
    ## note: using rdflib URIRefs
    col_name_iris_dict = \
        { key: URIRef(f'{base_iri}{key}') for key in col_names_dict.keys() }

    ## determine owl type for mixs terms
    if 'class' == term_type:
        sub_relation = RDFS.subClassOf
        owl_type = OWL.Class
    elif 'data property' == term_type:
        sub_relation = RDFS.subPropertyOf
        owl_type = OWL.DatatypeProperty
    else:
        raise Exception("You must supply a term type")

    ## build rdf graph from sheet
    graph = Graph()
    graph.add( (URIRef(ontology_iri), RDF.type, OWL.Ontology) )
    
    ## create mixs namespaces
    graph.namespace_manager.bind('mixs', base_iri) # binds mixs prefix to output
    mixs = Namespace(base_iri) # allows you to use mixs variable for iris (e.g.: mixs.mixs_version)

    ## add top leve iris for classes/properties
    top_term_iri, top_package_iri = _make_top_level_iris(graph)
    
    ## add package iri
    package_iri =  _make_pakage_iri(graph)

    ## add annaotiaon properties to graph
    graph = _make_annotation_properties(graph)
    
    ## add rows in sheet to graph
    graph = _make_triples(graph, sheet_df)
    
    return graph


def mixs_package_file_to_rdf (
        file_name,
        mixs_version,
        package_name="",
        term_type="class",
        file_type="excel",
        sep="\t",
        base_iri="https://gensc.org/mixs#",
        ontology_iri='https://gensc.org/mixs.owl',
        output_file="",
        ontology_format="turtle",
        print_output=False):
    """ 
    Builds an ontology (rdflib graph) from a MIxS package file.
    
    Args:
        file_name: The name of MIxS package file.
        mixs_version: The version of MIxS package.
        package_name: Overrides the package name provided in the package Excel spreadsheet.
                      This argument if necessary when using a file is a csv or tsv.
        term_type: Specifies if the MIxS terms will be represented as classes or data properties.
                   Accepted values: 'class', 'data property'
                   Default: 'class'
        file_type: The type of file being processed. 
                   If file type is not 'excel', a field separator/delimitor must be provided.
                   Default: 'excel'
        sep: Specifies the field separator/delimitor for non-Excel files.
        base_iri: The IRI used as prefix for MIxS terms.
        ontology_iri: The IRI used for the output ontology.
        output_file: The file used to save the output. 
                     If saving to different directory, include the path (e.g., '../output/mixs.ttl').
        ontology_format: The rdf syntax of the output ontology.
                   Accepted values: 'turtle', 'ttl', 'nt', 'ntriples', 'trix', 'json-ld', 'xml'
                   Default: 'turtle'
        print_output: Specifies whether to print ontology on screen.
                      Default: False
    Returns:
      rdflib Graph
    """
    
    ## recent mixs files are stored as Excel files
    if "excel" == file_type.lower():
        mixs_file = pds.read_excel(file_name, sheet_name=None) # load Excel file

        ## the package_name is displayed on the second sheet
        if "" == package_name.strip():
            package_name = list(mixs_file.keys())[1]

            ## create dataframe from second sheet
            mixs_sheet_df = mixs_file[package_name]
    else:
        ## non-Excel files require a package name
        if "" == package_name.strip():
            return "For non-Excel files, you must supply a package name"
        mixs_sheet_df = pds.read_csv(file_name, sep=sep)
        
    graph = mixs_sheet_df_to_rdf(mixs_sheet_df,
                                mixs_version,
                                package_name=package_name,
                                file_name=file_name,
                                term_type=term_type,
                                base_iri=base_iri,
                                ontology_iri=ontology_iri,
                                ontology_format=ontology_format)

    ## save rdf
    if "" != output_file:
        graph.serialize(format=ontology_format, destination=output_file)

    ## print output to screen
    if print_output:
        print(graph.serialize(format=ontology_format).decode('utf-8'))

    return graph



def mixs_package_directory_to_rdf (
        package_directory,
        mixs_version,
        term_type="class",
        file_name_start="M",
        file_type="excel",
        sep="\t",
        base_iri="https://gensc.org/mixs#",
        ontology_iri='https://gensc.org/mixs.owl',
        output_file="",
        ontology_format="turtle",
        print_output=False):
    """ 
    Builds an ontology (rdflib graph) from each Excel file in the specified package diretory.
    The graph retured is a union of each of the graphs builts from each file.
    
    Args:
        package_directory: The directory containing the MIxS package files.
        mixs_version: The version of MIxS package.
        package_name: Overrides the package name provided in the package Excel spreadsheet.
                      This argument if necessary when using a file is a csv or tsv.
        term_type: Specifies if the MIxS terms will be represented as classes or data properties.
                   Accepted values: 'class', 'data property'
                   Default: 'class'
        file_name_start: Specifies the letters the MIxS files should start with. The purpose is to avoid
                         retrieving unwanted system files, such as .DS_Store.
                         Default: 'M'
        file_type: The type of file being processed. 
                   If file type is not 'excel', a field separator/delimitor must be provided.
                   Default: 'excel'
        sep: Specifies the field separator/delimitor for non-Excel files.
        base_iri: The IRI used as prefix for MIxS terms.
        ontology_iri: The IRI used for the output ontology.
        output_file: The file used to save the output. 
                     If saving to different directory, include the path (e.g., '../output/mixs.ttl').
        ontology_format: The rdf syntax of the output ontology.
                         Accepted values: 'turtle', 'ttl', 'nt', 'ntriples', 'trix', 'json-ld', 'xml'
                         Default: 'turtle'
        print_output: Specifies whether to print ontology on screen.
                      Default: False
     Returns:
      rdflib Graph
    """

    ## get files in directory
    ## os.walk() returns tuple root, dirs, files; so use [2];
    ## see: https://www.tutorialspoint.com/python/os_walk.htm
    # next() function returns the next item in an iterator
    #pacpkage_files = next(os.walk(package_directory))[2]
    package_files = next(os.walk(package_directory))[2]

    ##  check if beginning of file name is specified
    ## this is to avoid unwanted files such as .DS_Store
    if '' != file_name_start:
        package_files = [file_name for file_name in package_files if 'M' == file_name[0]]
    #print(package_files) # testing
    
    ## build graph out of all package files
    package_graph = Graph()
    package_graph.add( (URIRef(ontology_iri), RDF.type, OWL.Ontology) )

    ## create mixs namespaces for package graph
    package_graph.namespace_manager.bind('mixs', base_iri) # binds mixs prefix to output
    mixs = Namespace(base_iri) # allows you to use mixs variable for iris (e.g.: mixs.mixs_version)
    
    for file_name in package_files:
        package_file = os.path.abspath(f'{package_directory}{file_name}')
        print('processing:', file_name)
        
        package_graph +=  \
            mixs_package_file_to_rdf (
                file_name=package_file,
                mixs_version=mixs_version,
                package_name="",
                term_type=term_type,
                file_type=file_type,
                sep=sep,
                base_iri=base_iri,
                ontology_iri=ontology_iri,
                ontology_format=ontology_format)
            
    ## save rdf
    if "" != output_file:
        package_graph.serialize(format=ontology_format, destination=output_file)

    ## print output to screen
    if print_output:
        print(package_graph.serialize(format=ontology_format).decode('utf-8'))


    return package_graph


def mixs_combined_file_to_rdf(
        file_name,
        mixs_version,
        package_name="",
        term_type="class",
        file_format="excel",
        sep="\t",
        base_iri="https://gensc.org/mixs#",
        ontology_iri='https://gensc.org/mixs.owl'):
    """
    TO DO: Builds an ontology (rdf_etl graph) from a MIxS fil which contians all the packages in an Excel spreadsheet.
    """
    pass


def mixs_package_df_to_rdf (
        package_df,
        package_name,
        mixs_version,
        term_type="class",
        base_iri="https://gensc.org/mixs#",
        ontology_iri='https://gensc.org/mixs.owl'):
    """
    TO DO: Builds an ontology (rdflib graph) from a MIxS package dataframe.
    """
    pass


if '__main__' == __name__:
    #print('cwd', os.path.abspath(os.curdir))
    
    ## make sure you are in dev diretory
    os.chdir('/Users/wdduncan/repos/mixs/mixs-rdf/src/code/mixs_to_rdf')
    #print(os.getcwd())

    ## test using single package filen
    test_file = "../../mixs_data/mixs_v5_packages/MIxSair_20180621.xlsx"
    #mixs_package_file_to_rdf(test_file, 5, output_file='test.ttl')
    #mixs_package_file_to_rdf (test_file, 5, term_type='data property', output_file='test.ttl')

    ## test using directory with package files
    test_directory = "../../mixs_data/mixs_v5_packages/"
    #mixs_package_directory_to_rdf(test_directory, 5, output_file='test.ttl')
