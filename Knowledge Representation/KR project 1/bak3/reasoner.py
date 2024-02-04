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

class ELReasoner:
    def __init__(self, ontology_file, class_name):
        self.ontology_file = ontology_file
        self.class_name = class_name
        self.interpretation = Interpretation()
        self.interpretation.create_new_element(class_name)

        self.gateway = JavaGateway()
        self.formatter = self.gateway.getSimpleDLFormatter()
        self.elFactory = self.gateway.getELFactory()

        self.ontology = self.gateway.getOWLParser().parseFile(ontology_file)
        self.trim_tbox()
        self.cls_dict ={self.formatter.format(concept):concept for concept in self.ontology.getSubConcepts()}

    def trim_tbox(self):
        axioms = self.tbox.getAxioms()
        for axiom in axioms:
            axiomType = axiom.getClass().getSimpleName()
            if axiomType == "EquivalenceAxiom":
                sides = axiom.getConcepts()
                l2r = self.elFactory.getGCI(sides[0], sides[1])
                r2l = self.elFactory.getGCI(sides[1], sides[0])
                self.tbox.add(l2r)
                self.tbox.add(r2l)
                self.ontology.remove(axiom)
            elif axiomType != "GeneralConceptInclusion":
                self.ontology.remove(axiom)
    
    def apply_rule_1(self):
        changed = False
        for d in self.interpretation.nodes:
            if '⊤' not in self.interpretation.get_node_labels(d):
                self.interpretation.add_concept_to_node(d,'⊤')
                changed = True
        return changed

    def get_subsumers(self):
        subsumers = set()

        changed = True
        while changed:
            changed = False
            if self.apply_rule_1():
                changed = True

        conceptNames = [self.formatter.format(x) for x in self.ontology.getConceptNames()]
        conceptNames += ['⊤']

        for concept in self.interpretation.get_node_labels('d0'):
            if concept in conceptNames:
                subsumers.add(concept)

        return subsumers

def parse_arguments():
    parser = argparse.ArgumentParser(description='EL Reasoner')
    parser.add_argument('ontology_file', type=str, help='Path to the ontology file')
    parser.add_argument('class_name', type=str, help='The class name to reason about')
    return parser.parse_args()

def main():
    args = parse_arguments()
    ontology_file = args.ontology_file
    class_name = args.class_name
    reasoner = ELReasoner(ontology_file, class_name)
    subsumers = reasoner.get_subsumers()
    for subsumer in subsumers:
        print(subsumer)

if __name__ == "__main__":
    main()