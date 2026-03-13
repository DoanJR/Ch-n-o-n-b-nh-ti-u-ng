import re

def extract_entities(text):

    diseases = []
    symptoms = []
    drugs = []
    tests = []

    lines = text.split("\n")

    for line in lines:

        if "triệu chứng" in line.lower():
            symptoms.append(line)

        if "thuốc" in line.lower():
            drugs.append(line)

        if "xét nghiệm" in line.lower():
            tests.append(line)

    diseases.append("Tiểu đường")

    return {
        "disease": diseases,
        "symptoms": symptoms,
        "drugs": drugs,
        "tests": tests
    }