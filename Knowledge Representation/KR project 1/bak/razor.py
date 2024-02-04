from py4j.java_gateway import JavaGateway

# def load_ontology(file_path):

#     gateway = JavaGateway()
#     parser = gateway.getOWLParser()
#     ontology = parser.parseFile(file_path)
#     return ontology

gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
# ontology = parser.parseFile("first_draft.owl")
ontology = parser.parseFile("pizza.owl")

tbox = ontology.tbox()
axioms = tbox.getAxioms()
# for axiom in axioms:
#     print(formatter.format(axiom))

allConcepts = ontology.getSubConcepts()
# print()
# print("There are ", len(allConcepts), " concepts occurring in the ontology")
# print("These are the concepts occurring in the ontology:")
# print([formatter.format(x) for x in allConcepts])

# conceptNames = ontology.getConceptNames()
# print()
# print("There are ", len(conceptNames), " concept names occurring in the ontology")
# print("These are the concept names: ")
# print([formatter.format(x) for x in conceptNames])

# foundGCI = False
# foundEquivalenceAxiom = False
# print()
# print("Looking for axiom types in EL")
# for axiom in axioms:
#     axiomType = axiom.getClass().getSimpleName()
#     if not foundGCI and axiomType == "GeneralConceptInclusion":
#         print("I found a general concept inclusion:")
#         print(formatter.format(axiom))
#         print("The left hand side of the axiom is: ", formatter.format(axiom.lhs()))
#         print("The right hand side of the axiom is: ", formatter.format(axiom.rhs()))
#         print()
#         foundGCI = True
#     elif not foundEquivalenceAxiom and axiomType == "EquivalenceAxiom":
#         print("I found an equivalence axiom:")
#         print(formatter.format(axiom))
#         print("The concepts made equivalent are: ")
#         for concept in axiom.getConcepts():
#             print(" - "+formatter.format(concept))
#         print()
#         foundEquivalenceAxiom = True

# foundConceptName = False
# foundTop = False
# foundExistential = False
# foundConjunction = False
# foundConceptTypes = set()
# print()
# print("Looking for concept types in EL")
# for concept in allConcepts:
#     conceptType = concept.getClass().getSimpleName()
#     if conceptType not in foundConceptTypes:
#         print(conceptType)
#         foundConceptTypes.add(conceptType)
#         if not foundConceptName and conceptType == "ConceptName":
#             print("I found a concept name: "+formatter.format(concept))
#             print()
#             foundConceptName = True
#         elif not foundTop and conceptType == "TopConcept$":
#             print("I found the top concept: "+formatter.format(concept))
#             print()
#             foundTop = True
#         elif not foundExistential and conceptType == "ExistentialRoleRestriction":
#             print("I found an existential role restriction: "+formatter.format(concept))
#             print("The role is: "+formatter.format(concept.role()))
#             print("The filler is: "+formatter.format(concept.filler()))
#             print()
#             foundExistential = True
#         elif not foundConjunction and conceptType == "ConceptConjunction":
#             print("I found a conjunction: "+formatter.format(concept))
#             print("The conjuncts are: ")
#             for conjunct in concept.getConjuncts():
#                 print(" - "+formatter.format(conjunct))
#             print()
#             foundConjunction = True

# elFactory = gateway.getELFactory()
# conceptA = elFactory.getConceptName("A")
# conceptB = elFactory.getConceptName("B")
# conjunctionAB = elFactory.getConjunction(conceptA, conceptB)
# role = elFactory.getRole("r")
# existential = elFactory.getExistentialRoleRestriction(role, conjunctionAB)
# top = elFactory.getTop()
# conjunction2 = elFactory.getConjunction(top, existential)
# gci = elFactory.getGCI(conjunctionAB, conjunction2)

# print()
# print("I made the following GCI:")
# print(formatter.format(gci))

