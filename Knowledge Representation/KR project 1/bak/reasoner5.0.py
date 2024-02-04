from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
ontology = parser.parseFile("pizza.owl")
gateway.convertToBinaryConjunctions(ontology)

allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()
axioms = ontology.tbox().getAxioms()

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


elFactory = gateway.getELFactory()
class_name = '"Pizza" ⊓ ∀hasBase."ThinAndCrispyBase"'
individuals = [Individual('d0')]
individuals[0].assign_concept(elFactory.getConceptName(class_name))


def apply_t_rule(individuals):
    top_concept = elFactory.getConceptName('⊤')
    for d in individuals:
        d.assign_concept(top_concept)


def apply_and_rule_1(individuals):
    for d in individuals:        
        for concept in d.concepts:
            conceptType = concept.getClass().getSimpleName()
            if conceptType == "ConceptConjunction":
            	print(concept)
            	for conjunct in concept.getConjuncts():            		
            		d.assign_concept(conjuct)

apply_t_rule(individuals)
apply_and_rule_1(individuals)

for concept in individuals[0].concepts:
    print(formatter.format(concept))