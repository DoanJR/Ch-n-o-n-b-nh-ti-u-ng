from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "Doanjr3105@"


def create_graph(data):

    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

    with driver.session() as session:

        disease = data["disease"][0]

        session.run(
            "MERGE (d:Disease {name:$name})",
            name=disease
        )

        for s in data["symptoms"]:
            session.run("""
                MERGE (sym:Symptom {name:$sym})
                WITH sym
                MATCH (d:Disease {name:$disease})
                MERGE (d)-[:HAS_SYMPTOM]->(sym)
            """, sym=s, disease=disease)

        for drug in data["drugs"]:
            session.run("""
                MERGE (dr:Drug {name:$drug})
                WITH dr
                MATCH (d:Disease {name:$disease})
                MERGE (d)-[:TREATED_BY]->(dr)
            """, drug=drug, disease=disease)

        for t in data["tests"]:
            session.run("""
                MERGE (te:Test {name:$test})
                WITH te
                MATCH (d:Disease {name:$disease})
                MERGE (d)-[:DIAGNOSED_BY]->(te)
            """, test=t, disease=disease)

    driver.close()

    print("Graph created!")