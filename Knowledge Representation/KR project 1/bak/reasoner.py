import argparse
from py4j.java_gateway import JavaGateway

def load_ontology(file_path):

    gateway = JavaGateway()
    parser = gateway.getOWLParser()
    ontology = parser.parseFile(file_path)
    return ontology

def apply_inference_rules(ontology, class_name):

    elements = { "d0": {class_name} }
    changed = True

    while changed:
        changed = False

        for d in elements:
            concepts = elements[d]

            if "⊤" not in concepts:
                concepts.add("⊤")
                changed = True

            for concept in list(concepts):
                if "⊓" in concept:
                    c1, c2 = concept.split("⊓")
                    if c1 not in concepts:
                        concepts.add(c1)
                        changed = True
                    if c2 not in concepts:
                        concepts.add(c2)
                        changed = True

            elements[d] = concepts

    return concepts in elements["d0"]


def el_reasoner(ontology_file, class_name):
    ontology = load_ontology(ontology_file)
    subsumers = apply_inference_rules(ontology, class_name)
    return subsumers

def main():
    parser = argparse.ArgumentParser(description='EL Reasoner')
    parser.add_argument('ontology_file', type=str, help='Path to the OWL ontology file')
    parser.add_argument('class_name', type=str, help='Class name to check for subsumers')
    args = parser.parse_args()

    subsumers = el_reasoner(args.ontology_file, args.class_name)
    for subsumer in subsumers:
        print(subsumer)

if __name__ == "__main__":
    main()