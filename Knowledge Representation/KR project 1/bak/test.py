from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
# ontology = parser.parseFile("first_draft.owl")
ontology = parser.parseFile("pizza.owl")

tbox = ontology.tbox()
axioms = tbox.getAxioms()

allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()