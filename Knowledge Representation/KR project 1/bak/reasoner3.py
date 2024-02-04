from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
# ontology = parser.parseFile("first_draft.owl")
ontology = parser.parseFile("pizza.owl")
gateway.convertToBinaryConjunctions(ontology)

tbox = ontology.tbox()
axioms = tbox.getAxioms()

allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()

# ontology_class = ontology.getClass().getSimpleName()
# print(ontology_class)

# for axiom in axioms:
#     print(formatter.format(axiom))

class_name = "Margherita"

elFactory = gateway.getELFactory()
C0 = elFactory.getConceptName(class_name)
d0 = set()
d0.add(C0)
print(d0)