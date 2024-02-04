#! /usr/bin/python
from py4j.java_gateway import JavaGateway

# connect to the java gateway of dl4python
gateway = JavaGateway()

# get a parser from OWL files to DL ontologies
parser = gateway.getOWLParser()

# get a formatter to print in nice DL format
formatter = gateway.getSimpleDLFormatter()


ontology = parser.parseFile("pizza.owl")


gateway.convertToBinaryConjunctions(ontology)


tbox = ontology.tbox()
axioms = tbox.getAxioms()
concepts = ontology.getSubConcepts()


elFactory = gateway.getELFactory()

c="CheesyPizza"

conceptNames = [formatter.format(x) for x in ontology.getConceptNames()]+['⊤']
print(conceptNames)
# for axiom in axioms:
#     axiomType = axiom.getClass().getSimpleName()
#     if axiomType == "GeneralConceptInclusion":
#         C = formatter.format(axiom.lhs())
#         D = formatter.format(axiom.rhs())
#         if c in C or c in D:
#         	print(C, D)
        
#     elif axiomType == "EquivalenceAxiom":
#     	print(formatter.format(axiom))

# print('Good job!')
# print(tbox.size())

# for axiom in axioms:
#     axiomType = axiom.getClass().getSimpleName()            
#     if axiomType == "EquivalenceAxiom":
#         sides = axiom.getConcepts()
#         l2r = elFactory.getGCI(sides[0], sides[1])                
#         r2l = elFactory.getGCI(sides[1], sides[0])                
#         tbox.add(l2r)
#         tbox.add(r2l)
#         ontology.remove(axiom)
#     elif axiomType != "GeneralConceptInclusion":
#         ontology.remove(axiom)

# print(tbox.size())

# axioms = tbox.getAxioms()
# for axiom in axioms:
#     axiomType = axiom.getClass().getSimpleName()
#     if axiomType == "GeneralConceptInclusion":
#         C = formatter.format(axiom.lhs())
#         D = formatter.format(axiom.rhs())
#         if c in C or c in D:
#             print(C, D)
        
#     elif axiomType == "EquivalenceAxiom":
#         print(formatter.format(axiom))



# for concept in concepts:            
#     if formatter.format(concept)=='"CheesyPizza"':
#         print('Fuck!')