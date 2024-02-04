from py4j.java_gateway import JavaGateway

gateway = JavaGateway()
parser = gateway.getOWLParser()
formatter = gateway.getSimpleDLFormatter()
# ontology = parser.parseFile("first_draft.owl")
ontology = parser.parseFile("pizza.owl")

tbox = ontology.tbox()
axioms = tbox.getAxioms()
for axiom in axioms:
    print(formatter.format(axiom))

allConcepts = ontology.getSubConcepts()
conceptNames = ontology.getConceptNames()

class ELReasoner:
    def __init__(self, ontology):
        self.ontology = ontology
        self.changed = True

    def apply_rules(self):
        while self.changed:
            self.changed = False
            for d in list(self.ontology.keys()):
                concepts = self.ontology[d]

                # T-rule: Add top concept to any individual.
                if '⊤' not in concepts:
                    concepts.add('⊤')
                    self.changed = True

                # Π-rule 1: If d has C ∧ D assigned, assign also C and D to d.
                to_add = set()
                for concept in concepts:
                    if '∧' in concept:
                        parts = concept.split('∧')
                        to_add.update(parts)
                if to_add:
                    self.ontology[d].update(to_add)
                    self.changed = True

                # Π-rule 2: If d has C and D assigned, assign also C ∧ D to d.
                for c1 in concepts:
                    for c2 in concepts:
                        new_concept = f"{c1}∧{c2}"
                        if new_concept not in concepts:
                            concepts.add(new_concept)
                            self.changed = True

                # ∃-rule 1: If d has ∃r.C assigned and there's no r-successor, create one and assign C.
                for concept in concepts:
                    if concept.startswith('∃'):
                        _, r, C = concept.partition('.')
                        r_successor = f"{d}.{r}"
                        if r_successor not in self.ontology:
                            self.ontology[r_successor] = {C}
                            self.changed = True

                # ∃-rule 2: If d has an r-successor with C assigned, add ∃r.C to d.
                for other_d in self.ontology:
                    if other_d.startswith(f"{d}."):
                        r = other_d.split('.')[1]
                        for C in self.ontology[other_d]:
                            new_concept = f"∃{r}.{C}"
                            if new_concept not in concepts:
                                concepts.add(new_concept)
                                self.changed = True

                # ⊑-rule: If d has C assigned and C ⊑ D ∈ T, then also assign D to d.
                # Note: The Tbox should be provided separately, for this example, we'll simulate it.
                Tbox = {'C': 'D'}  # Assuming C is subsumed by D.
                for C in concepts:
                    if C in Tbox:
                        D = Tbox[C]
                        if D not in concepts:
                            concepts.add(D)
                            self.changed = True

    def reason(self):
        self.apply_rules()
        return self.ontology

# Example usage:
# ontology = {'d0': {'A'}}
# This is a very simplified example. In a real ontology, you would have complex relationships and rules.
# The ontology should be loaded from the 'pizza.owl' file in a proper format that the reasoner can use.
ontology = {'d0': {'C∧D', '∃r.C'}}
reasoner = ELReasoner(ontology)
result = reasoner.reason()
result
