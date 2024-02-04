from py4j.java_gateway import JavaGateway


class Concept:
    def __init__(self, name):
        self.name = name
        self.super_concepts = set()
        self.sub_concepts = set()

    def add_super_concept(self, super_concept):
        self.super_concepts.add(super_concept)

class TBox:
    def __init__(self):
        self.concepts = {}

    def get_concept(self, concept_name):
        if concept_name not in self.concepts:
            self.concepts[concept_name] = Concept(concept_name)
        return self.concepts[concept_name]

    def add_subsumption(self, sub_concept_name, super_concept_name):
        sub_concept = self.get_concept(sub_concept_name)
        super_concept = self.get_concept(super_concept_name)
        sub_concept.add_super_concept(super_concept)



gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
ontology = parser.parseFile("pizza.owl")
gateway.convertToBinaryConjunctions(ontology)

conceptNames = ontology.getConceptNames()
axioms = ontology.tbox().getAxioms()

tbox = TBox()

for concept_name in conceptNames:
    tbox.get_concept(formatter.format(concept_name))

for axiom in axioms:
    axiomType = axiom.getClass().getSimpleName()
    if axiomType == "GeneralConceptInclusion":
        lhs_concept = formatter.format(axiom.lhs())
        rhs_concept = formatter.format(axiom.rhs())
        tbox.add_subsumption(lhs_concept, rhs_concept)

# def print_tbox(tbox):
#     for concept_name, concept in tbox.concepts.items():
#         super_concepts = ', '.join([super_concept.name for super_concept in concept.super_concepts])
#         print(f"概念 '{concept_name}' 的超概念: {super_concepts}")

# print_tbox(tbox)


class Individual:
    def __init__(self, name):
        self.name = name
        self.concepts = set()
        self.role_successors = {}

    def assign_concept(self, concept):
        self.concepts.add(concept)

    def add_role_successor(self, role, successor):
        if role not in self.role_successors:
            self.role_successors[role] = []
        self.role_successors[role].append(successor)


class_name = '"Pizza" ⊓ ∀hasBase."ThinAndCrispyBase"'
individuals = [Individual('d0')]
individuals[0].assign_concept(tbox.get_concept(class_name))

# for concept in tbox.concepts:
#     print(concept)

def apply_t_rule(individuals):
    top_concept = Concept('⊤')
    for d in individuals:
        d.assign_concept(top_concept)

elFactory = gateway.getELFactory()

# def apply_and_rule_1(individuals):
#     for d in individuals:        
#         for c in list(d.concepts):        
#             print(c.name)    
#             concept = elFactory.getConceptName(c.name)
#             concept_type = concept.getClass().getSimpleName()
#             print(concept_type)
            # if concept_type == "ConceptConjunction":
            #     print("I found a conjunction: "+formatter.format(concept))
            #     print("The conjuncts are: ")
            #     for conjunct in concept.getConjuncts():
            #         print(" - "+formatter.format(conjunct))

apply_t_rule(individuals)

# for c in individuals[0].concepts:
#     print(c.name)

# for axiom in axioms:
#     axiomType = axiom.getClass().getSimpleName()
#     if axiomType == "EquivalenceAxiom":
#         print(formatter.format(axiom))
#         print(axiomType)
allConcepts = ontology.getSubConcepts()
for concept in allConcepts:
    conceptType = concept.getClass().getSimpleName()
    if conceptType == "ConceptConjunction":
        print(formatter.format(concept))