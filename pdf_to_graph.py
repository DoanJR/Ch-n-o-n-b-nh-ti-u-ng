from extract_pdf import extract_text_from_pdf
from entity_extraction import extract_entities
from neo4j_insert import create_graph


pdf_path = "diabet_data.pdf"

print("Reading PDF...")
text = extract_text_from_pdf(pdf_path)

print("Extracting entities...")
entities = extract_entities(text)

print("Creating graph...")
create_graph(entities)

print("Done!")