import random
from py4j.java_gateway import JavaGateway
from itertools import combinations
import argparse


class ELReasoner:
    def __init__(self, ontology_file, class_name=None):
        self.ontology_file = ontology_file
        self.class_name = class_name
        self.gateway = JavaGateway()
        self.formatter = self.gateway.getSimpleDLFormatter()
        self.elFactory = self.gateway.getELFactory()
        self.ontology = self.gateway.getOWLParser().parseFile(ontology_file)
        self.interpretation = Interpretation()
        self.concepts_dict = {}
        self.conjunction_dict = {}
        self.existential_dict = {}
        self.axioms_dict = {}

    def process_ontology(self):
        tbox = self.ontology.tbox()
        axioms = tbox.getAxioms()
        for axiom in axioms:
            axiomType = axiom.getClass().getSimpleName()
            if axiomType == "EquivalenceAxiom":
                sides = axiom.getConcepts()
                l2r = self.elFactory.getGCI(sides[0], sides[1])
                r2l = self.elFactory.getGCI(sides[1], sides[0])
                tbox.add(l2r)
                tbox.add(r2l)
                self.ontology.remove(axiom)
            elif axiomType != "GeneralConceptInclusion":
                self.ontology.remove(axiom)

        for concept in self.ontology.getSubConcepts():
            formatted_concept = self.formatter.format(concept)
            conceptType = concept.getClass().getSimpleName()
            self.concepts_dict[formatted_concept] = {
                'concept': concept,
                'conceptType': concept.getClass().getSimpleName()
            }
            if conceptType == "ConceptConjunction":
                self.conjunction_dict[formatted_concept] = {
                    'left': self.formatter.format(concept.getConjuncts()[0]),
                    'right': self.formatter.format(concept.getConjuncts()[1])
                }
            if conceptType == "ExistentialRoleRestriction":
                self.existential_dict[formatted_concept] = {
                    'role': self.formatter.format(concept.role()),
                    'filter': self.formatter.format(concept.filler())
                }

        for axiom in tbox.getAxioms():
            lhs_formatted = self.formatter.format(axiom.lhs())
            rhs_formatted = self.formatter.format(axiom.rhs())

            if lhs_formatted not in self.axioms_dict:
                self.axioms_dict[lhs_formatted] = []

            self.axioms_dict[lhs_formatted].append(rhs_formatted)

    def apply_rule_1(self):
        changed = False
        for d in self.interpretation.nodes:
            if '⊤' not in self.interpretation.get_node_labels(d):
                self.interpretation.add_concept_to_node(d, '⊤')
                changed = True
        return changed

    def apply_rule_2(self):
        changed = False
        for d in self.interpretation.nodes:
            concepts = self.interpretation.get_node_labels(d).copy()
            for concept in concepts:
                if concept in self.conjunction_dict.keys():
                    if self.conjunction_dict[concept]['left'] not in concepts:
                        self.interpretation.add_concept_to_node(d, self.conjunction_dict[concept]['left'])
                        changed = True
                    if self.conjunction_dict[concept]['right'] not in concepts:
                        self.interpretation.add_concept_to_node(d, self.conjunction_dict[concept]['right'])
                        changed = True
        return changed

    def apply_rule_3(self):
        changed = False
        for d in self.interpretation.nodes:
            concepts = self.interpretation.get_node_labels(d).copy()
            concepts.remove('⊤')
            pairs = list(combinations(concepts, 2))
            for A, B in pairs:
                if ('(' + A + ' ⊓ ' + B + ')' not in concepts) and ('(' + B + ' ⊓ ' + A + ')' not in concepts):
                    if '(' + A + ' ⊓ ' + B + ')' in self.concepts_dict.keys():
                        self.interpretation.add_concept_to_node(d, '(' + A + ' ⊓ ' + B + ')')
                        changed = True
                    elif '(' + B + ' ⊓ ' + A + ')' in self.concepts_dict.keys():
                        self.interpretation.add_concept_to_node(d, '(' + B + ' ⊓ ' + A + ')')
                        changed = True
        return changed

    def apply_rule_4(self):
        changed = False
        for d in list(self.interpretation.nodes):
            concepts = self.interpretation.get_node_labels(d).copy()
            for concept in concepts & self.existential_dict.keys():
                role = self.existential_dict[concept]['role']
                filter = self.existential_dict[concept]['filter']
                existing_successor = None
                for (source, target), roles in self.interpretation.edges.items():
                    if source == d and role in roles and filter in self.interpretation.get_node_labels(target):
                        existing_successor = target
                        break
                if not existing_successor:
                    new_node = self.interpretation.create_new_element(filter)
                    self.interpretation.add_edge(d, new_node, role)
                    changed = True
        return changed

    def apply_rule_5(self):
        changed = False
        for (source, target), roles in self.interpretation.edges.items():
            concept_s = self.interpretation.get_node_labels(source)
            concept_t = self.interpretation.get_node_labels(target)
            for role in roles:
                new_labels = set(['∃' + role + '.' + c for c in concept_t]) & self.concepts_dict.keys() - concept_s
                for label in new_labels:
                    self.interpretation.add_concept_to_node(source, label)
                    changed = True
        return changed

    def apply_rule_6(self):
        changed = False
        for d in self.interpretation.nodes:
            concepts = self.interpretation.get_node_labels(d).copy()
            for concept in (concepts & self.axioms_dict.keys()):
                for D in self.axioms_dict[concept]:
                    if D not in concepts:
                        self.interpretation.add_concept_to_node(d, D)
                        changed = True
        return changed

    def run(self):
        if not self.class_name:
            self.class_name = random.choice(list(self.concepts_dict.keys()))

        self.process_ontology()

        self.interpretation.create_new_element(self.class_name)
        changed = True
        while changed:
            changed = False
            changed |= self.apply_rule_1()
            changed |= self.apply_rule_2()
            changed |= self.apply_rule_3()
            changed |= self.apply_rule_4()
            changed |= self.apply_rule_5()
            changed |= self.apply_rule_6()

        subsumers = set()
        conceptNames = [self.formatter.format(x) for x in self.ontology.getConceptNames()]
        for concept in self.interpretation.get_node_labels('d0'):
            if concept in conceptNames:
                subsumers.add(concept)
        return subsumers


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="EL Reasoner")
    parser.add_argument("ontology_file", help="Path to the ontology file")
    parser.add_argument("class_name", help="Class name to reason about", default=None)
    args = parser.parse_args()

    reasoner = ELReasoner(args.ontology_file, args.class_name)
    subsumers = reasoner.run()
    for subsumer in subsumers:
        print(subsumer)