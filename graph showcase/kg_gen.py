import pandas as pd
import random

# Recreating the exact dataset for you
patients = [
    {"id": "S1001", "name": "Tan Wei Ling", "age": 72, "gender": "Female", "race": "Chinese", "religion": "Buddhist", "housing": "HDB 4-Room"},
    {"id": "S1002", "name": "Muhammad Syazwan", "age": 29, "gender": "Male", "race": "Malay", "religion": "Muslim", "housing": "HDB 5-Room"},
    {"id": "S1003", "name": "Rajendran s/o Muthu", "age": 58, "gender": "Male", "race": "Indian", "religion": "Hindu", "housing": "HDB 3-Room"},
    {"id": "S1004", "name": "Chloe de Souza", "age": 41, "gender": "Female", "race": "Eurasian", "religion": "Christian", "housing": "Condominium"},
    {"id": "S1005", "name": "Lim Boon Hock", "age": 84, "gender": "Male", "race": "Chinese", "religion": "Taoist", "housing": "HDB 2-Room (Rental)"}
]

complaints = ["Chest Pain", "Shortness of Breath", "Abdominal Pain", "Fall", "Fever", "Giddiness"]
dispositions = ["Discharged with 3 days MC", "Admitted to General Ward", "Referral to Specialist SOC", "Follow up at Polyclinic"]
diagnoses = ["Acute MI", "Pneumonia", "Gastroenteritis", "Hip Fracture", "Viral Fever", "BPPV"]

nodes, edges = [], []
for p in patients:
    nodes.append({'id': p['id'], 'label': 'Patient', 'name': p['name'], 'age': p['age'], 'gender': p['gender'], 'race': p['race'], 'religion': p['religion'], 'housing type': p['housing']})
    for i in range(1, 26):
        nid = f"Note_ED_{p['id']}_{i}"; comp = random.choice(complaints); disp = random.choice(dispositions)
        nodes.append({'id': nid, 'label': 'Note', 'type': 'ED', 'content': f"Patient presented with {comp}. {disp}."})
        edges.append({'source': p['id'], 'target': nid, 'type': 'HAS_NOTE'})
    for i in range(1, 26):
        nid = f"Note_DS_{p['id']}_{i}"; diag = random.choice(diagnoses)
        nodes.append({'id': nid, 'label': 'Note', 'type': 'DS', 'course': "Managed conservatively."})
        edges.append({'source': p['id'], 'target': nid, 'type': 'HAS_NOTE'})

pd.DataFrame(nodes).to_csv('kg_nodes.csv', index=False)
pd.DataFrame(edges).to_csv('kg_edges.csv', index=False)
print("Files created successfully.")