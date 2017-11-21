from lxml import etree
from rdflib import Namespace, Graph, URIRef, BNode, Literal, URIRef
from rdflib.namespace import DCTERMS, RDFS, RDF, DC, FOAF, SKOS
import pprint

ZinGraph = Graph()


# xmlschema_doc = etree.parse("data/basisschema.xsd")
xmlschema_doc = etree.parse("data/AW317.xsd")


root = xmlschema_doc.getroot()


for complexType in root.findall(".//{http://www.w3.org/2001/XMLSchema}complexType"):
        print(complexType.attrib["name"])
        URIRef(complexType.attrib["name"])
        description = complexType.find(".//{http://www.w3.org/2001/XMLSchema}documentation")
#        print(description.__dict__)
#        print(description.text)
        name = URIRef(complexType.attrib["name"])
        print(dir(description))
        if "text" in dir(description):
            ZinGraph.add((name, DCTERMS.description, Literal(description.text, lang="nl")))
            ZinGraph.add((name, RDFS.label, Literal(name.replace("CDT_", ""), lang="nl")))
        for element in complexType.findall(".//{http://www.w3.org/2001/XMLSchema}element"):
            element_name = URIRef(element.attrib["name"])
            ZinGraph.add((element_name, RDFS.label, Literal(element_name, lang="nl")))

            if "type" in element.attrib.keys():
                element_type = URIRef(element.attrib["type"].replace("iwlz:", "http://www.istandaarden.nl/iwlz/1_2/basisschema/schema/1_2/"))
                ZinGraph.add((element_name, RDF.type, element_type))


            ZinGraph.add((element_name, DCTERMS.isPartOf, name))

            #description2 = element.find(".//{http://www.w3.org/2001/XMLSchema}documentation")
            #print(description2.text)
        #for grandchild in child:
        #    print(grandchild.tag, grandchild.attrib)

# ZinGraph.serialize(destination='/tmp/Zin_basisschema.ttl', format='turtle')
ZinGraph.serialize(destination='/tmp/Zin_AW317.ttl', format='turtle')
