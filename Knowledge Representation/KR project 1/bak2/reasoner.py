import sys
from py4j.java_gateway import JavaGateway
from itertools import combinations
import argparse

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
        self.element_counter = 1

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
    def __init__(self, ontology_file, initial_concept): 
        self.ontology_file = ontology_file
        self.initial_concept = initial_concept
        self.interpretation = Interpretation()
        self.interpretation.add_node('d0', initial_concept)
        self.gateway = JavaGateway()
        self.formatter = self.gateway.getSimpleDLFormatter()
        self.elFactory = self.gateway.getELFactory()
        self.ontology = self.load_ontology(self.ontology_file)
        self.allConcepts = self.ontology.getSubConcepts()
        self.axioms = self.decompose_equivalence(self.ontology.tbox()).getAxioms()


    def load_ontology(self, ontology_file):        
        parser = self.gateway.getOWLParser()
        ontology = parser.parseFile(ontology_file)
        return ontology

    def get_concept(self, class_name):
        concepts = self.ontology.getSubConcepts()
        for c in concepts:            
            if self.formatter.format(c)==class_name:                
                return c

    def decompose_equivalence(self, tbox):        
        axioms = tbox.getAxioms()
        for axiom in axioms:
            axiomType = axiom.getClass().getSimpleName()            
            if axiomType == "EquivalenceAxiom":
                sides = axiom.getConcepts()
                l2r = self.elFactory.getGCI(sides[0], sides[1])                
                r2l = self.elFactory.getGCI(sides[1], sides[0])                
                tbox.add(l2r)
                tbox.add(r2l)                
        return tbox


    def apply_t_rule(self):
        changed = False
        for d in self.interpretation.nodes:
            if '⊤' not in self.interpretation.get_node_labels(d):
                self.interpretation.add_concept_to_node(d,'⊤')
                changed = True
        return changed

    def apply_and_rule1(self):
        changed = False        
        for d in self.interpretation.nodes:
            new_concepts = set()
            concepts = self.interpretation.get_node_labels(d).copy()
            
            for c in concepts:
                concept = self.get_concept(c)
                if concept:
                    conceptType = concept.getClass().getSimpleName()
                    if conceptType == "ConceptConjunction":
                        for conjunct in concept.getConjuncts():
                            formatted_conjunct = self.formatter.format(conjunct)
                            if formatted_conjunct not in concepts:
                                new_concepts.add(formatted_conjunct)

            for new_concept in new_concepts:                
                self.interpretation.add_concept_to_node(d, new_concept)
                changed = True              
        return changed

    def apply_and_rule2(self):
        changed = False 
        for d in self.interpretation.nodes:
            new_concepts = set()
            concepts = self.interpretation.get_node_labels(d).copy()

            cc = list(combinations(concepts,2))
            for i,j in cc:
                A=self.get_concept(i)                
                B=self.get_concept(j)
                if A and B:
                    conjunction=self.elFactory.getConjunction(A,B)
                    formatted_conjunction = self.formatter.format(conjunction)                    
                    if (formatted_conjunction in self.allConcepts) and (formatted_conjunction not in concepts):
                        new_concepts.add(formatted_conjunction)

            for new_concept in new_concepts:                
                self.interpretation.add_concept_to_node(d, new_concept)
                changed = True
        return changed

    def apply_some_rule1(self):
        changed = False
        for d in list(self.interpretation.nodes):               
            concepts = self.interpretation.get_node_labels(d).copy()            

            for c in concepts:                
                concept = self.get_concept(c)
                if concept:
                    conceptType = concept.getClass().getSimpleName()                    
                    if conceptType == "ExistentialRoleRestriction": 
                        role = self.formatter.format(concept.role())
                        fltr = self.formatter.format(concept.filler())
                        existing_successor = None
                        for (source, target), roles in self.interpretation.edges.items():
                            if source == d and role in roles and fltr in self.interpretation.get_node_labels(target):
                                existing_successor = target
                                break

                        if not existing_successor:                            
                            new_node = self.interpretation.create_new_element(fltr)
                            self.interpretation.add_edge(d, new_node, role)                            
                            changed = True
        return changed
                        
    def apply_some_rule2(self):
        changed = False        
        for d in list(self.interpretation.nodes):
            for (source, target), roles in self.interpretation.edges.items():
                if source == d:
                    for r in roles:                        
                        for concept in self.interpretation.get_node_labels(target):
                            role = self.elFactory.getRole(r)
                            fltr = self.elFactory.getConceptName(concept)
                            existential_concept = self.elFactory.getExistentialRoleRestriction(role, fltr)                            
                            if existential_concept in self.allConcepts:
                                concept_name=self.formatter.format(existential_concept)
                                if concept_name not in self.interpretation.get_node_labels(d):                                    
                                    self.interpretation.add_concept_to_node(d, existential_concept)
                                    changed = True
        return changed


    def apply_incl_rule(self):
        changed = False
        for d in self.interpretation.nodes:
            concepts = self.interpretation.get_node_labels(d).copy()
            for c in concepts:                
                for axiom in self.axioms:
                    axiomType = axiom.getClass().getSimpleName()
                    if axiomType=="GeneralConceptInclusion":
                        C = self.formatter.format(axiom.lhs())
                        D = self.formatter.format(axiom.rhs())                        
                        if (C in concepts) and (D not in concepts):                            
                            self.interpretation.add_concept_to_node(d, D)
                            changed = True               
        return changed



    def run(self):                           

        changed = True
        while changed:
            changed = False
            if self.apply_t_rule():
                changed = True
            if self.apply_and_rule1():
                changed = True
            if self.apply_and_rule2():
                changed = True
            if self.apply_some_rule1():
                changed = True
            if self.apply_some_rule2():
                changed = True
            if self.apply_incl_rule():
                changed = True

        return self.interpretation.get_node_labels('d0')

def parse_arguments():
    parser = argparse.ArgumentParser(description='EL Reasoner')
    parser.add_argument('ontology_file', type=str, help='Path to the ontology file')
    parser.add_argument('class_name', type=str, help='The class name to reason about')
    return parser.parse_args()

def main():
    ontology_file = 'pizza.owl'
    class_name = '("Pizza" ⊓ ∃hasTopping."SpicyTopping")'
    reasoner = ELReasoner(ontology_file, class_name)
    subsumers = reasoner.run()
    for subsumer in subsumers:
        print(subsumer)

# def main():
#     args = parse_arguments()
#     ontology_file = args.ontology_file
#     class_name = args.class_name

#     try:
#         reasoner = ELReasoner(ontology_file, class_name)
#         subsumers = reasoner.run()
#         for subsumer in subsumers:
#             print(subsumer)
#     except Exception as e:
#         print(f"Error occurred: {e}", file=sys.stderr)

# if __name__ == "__main__":
#     main()

# EXAMPLE:
# python reasoner.py pizza.owl '("Pizza" ⊓ ∃hasTopping."SpicyTopping")'