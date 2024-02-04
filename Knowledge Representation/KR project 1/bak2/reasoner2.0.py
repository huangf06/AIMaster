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
        self.axioms = self.trim_tbox(self.ontology.tbox()).getAxioms()


    def load_ontology(self, ontology_file):        
        parser = self.gateway.getOWLParser()
        ontology = parser.parseFile(ontology_file)
        return ontology

    def get_concept(self, class_name):
        concepts = self.ontology.getSubConcepts()
        for c in concepts:            
            if self.formatter.format(c)==class_name:                
                return c

    def trim_tbox(self, tbox):        
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
                    conjunction_init = self.get_concept(formatted_conjunction)
                    if (conjunction_init in self.allConcepts) and (formatted_conjunction not in concepts):
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
            new_concepts = set()

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
                                    new_concepts.add(concept_name)

            for new_concept in new_concepts:                
                self.interpretation.add_concept_to_node(d, new_concept)
                changed = True

        return changed


    def apply_gci_rule(self):
        changed = False
        for d in self.interpretation.nodes:
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


    def run(self):                           

        changed = True
        while changed:
            changed = False
            if self.apply_t_rule():
                # print("Rule1: t")
                changed = True
            if self.apply_and_rule1():
                # print("Rule2: and")
                changed = True
            if self.apply_and_rule2():
                # print("Rule3: and")
                changed = True
            if self.apply_some_rule1():
                # print("Rule4: some")
                changed = True
            if self.apply_some_rule2():
                # print("Rule5: some")
                changed = True
            if self.apply_gci_rule():
                # print("Rule6: gci")
                changed = True

        subsumers = set()
        conceptNames = [self.formatter.format(x) for x in self.ontology.getConceptNames()]
        conceptNames = conceptNames+['⊤']

        for label in self.interpretation.get_node_labels('d0'):
            if label in conceptNames:
                subsumers.add(label)

        return subsumers



# C0 = '("Pizza" ⊓ ∃hasTopping."SpicyTopping")'
C0 = '"Margherita"'
# C0 = 'Paper_Kebab'
reasoner = ELReasoner('pizza.owl',C0)
subsumers = reasoner.run()
for subsumer in subsumers:
    print(subsumer)