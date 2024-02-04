from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
ontology = parser.parseFile("pizza.owl")
gateway.convertToBinaryConjunctions(ontology)

allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()
axioms = ontology.tbox().getAxioms()

# Dictionary for storing concepts
concepts_dict = {}
for concept in allConcepts:
    concept_type = concept.getClass().getSimpleName()
    concept_name = formatter.format(concept)
    concepts_dict[concept_name] = {"object": concept,"type": concept_type}
    if concept_type=="ConceptConjunction ":
    	print(concept_name)
# print(concepts_dict['"Pizza" ⊓ ∀hasBase."ThinAndCrispyBase"'])

# # Dictionary for storing axioms
# axioms_dict = {}
# for axiom in axioms:
#     axiom_type = axiom.getClass().getSimpleName()
#     formatted_axiom = formatter.format(axiom)
#     if axiom_type == "GeneralConceptInclusion":
#         axioms_dict[formatted_axiom] = {
#             "type": axiom_type,
#             "lhs": formatter.format(axiom.lhs()),
#             "rhs": formatter.format(axiom.rhs())
#         }
#     elif axiom_type == "EquivalenceAxiom":
#         axioms_dict[formatted_axiom] = {
#             "type": axiom_type,
#             "concepts": [formatter.format(concept) for concept in axiom.getConcepts()]
#         }
