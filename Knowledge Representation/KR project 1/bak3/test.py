import sys
import argparse
from py4j.java_gateway import JavaGateway
from itertools import combinations

class DirectedLabeledGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, node, label=None):
        if node not in self.nodes:
            self.nodes[node] = set()                     
        if label:
            self.nodes[node].add(label)           

    def add_edge(self, source, target, label):
        if (source, target) not in self.edges:
            self.edges[(source, target)] = set()
        self.edges[(source, target)].add(label)

    def get_node_labels(self, node):
        return self.nodes.get(node, set())

    def get_edge_labels(self, source, target):
        return self.edges.get((source, target), set())


class Interpretation(DirectedLabeledGraph):
    def __init__(self):
        super().__init__()
        self.element_counter = 0

    def add_concept_to_node(self, node, concept):
        """Add a concept to a node."""
        if node not in self.nodes:
            self.add_node(node)
        self.nodes[node].add(concept)       
        return concept in self.nodes[node]

    def exists_edge(self, source, role, target):
        """Check if there exists an edge with a specific role between two nodes."""
        return role in self.get_edge_labels(source, target)

    def create_new_element(self, concept):
        """Create a new element with a specified concept."""
        new_element = f"d{self.element_counter}"
        self.element_counter += 1
        self.add_node(new_element, concept)        
        return new_element


ontology_file = 'pizza.owl'
class_name = '"Margherita"'		
interpretation = Interpretation()
interpretation.create_new_element(class_name)

gateway = JavaGateway()
formatter = gateway.getSimpleDLFormatter()
elFactory = gateway.getELFactory()

ontology = gateway.getOWLParser().parseFile(ontology_file)
concept_dict ={formatter.format(concept):concept for concept in ontology.getSubConcepts()}

axioms = ontology.tbox().getAxioms()
print("numbers of axioms before trim:", len(axioms))

for axiom in axioms:    
    axiomType = axiom.getClass().getSimpleName()            
    if axiomType == "EquivalenceAxiom":
        sides = axiom.getConcepts()
        l2r = elFactory.getGCI(sides[0], sides[1])                
        r2l = elFactory.getGCI(sides[1], sides[0])                
        ontology.tbox().add(l2r)
        ontology.tbox().add(r2l)
        ontology.remove(axiom)
    elif axiomType != "GeneralConceptInclusion":        
        ontology.remove(axiom)

axioms = ontology.tbox().getAxioms()
print("numbers of axioms after trim:", len(axioms))

def apply_gci_rule():
    changed = False
    for d in interpretation.nodes:
        new_concepts = set()

        concepts = self.interpretation.get_node_labels(d).copy()
        for axiom in self.axioms:
            C = self.formatter.format(axiom.lhs())
            D = self.formatter.format(axiom.rhs())    
            if (C in concepts) and (D not in concepts) and C!='⊤':
                new_concepts.add(D)

        for new_concept in new_concepts:                
            self.interpretation.add_concept_to_node(d, new_concept)
            changed = True

    return changed

subsumers = set()       

changed = True
while changed:
    changed = False
    if apply_rule_1():
        changed = True

conceptNames = [formatter.format(x) for x in ontology.getConceptNames()]
conceptNames += ['⊤']

for concept in interpretation.get_node_labels('d0'):
    if concept in conceptNames:
        subsumers.add(concept)

for subsumer in subsumers:
    print(subsumer)