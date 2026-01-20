import pandas as pd
import random

# 1. Setup Patient Data (Same 10 personas)
patients_data = [
    {"id": "S1001", "name": "Tan Wei Ling", "age": 72, "gender": "Female", "race": "Chinese", "religion": "Buddhist", "has_rmd": True},
    {"id": "S1002", "name": "Muhammad Syazwan", "age": 29, "gender": "Male", "race": "Malay", "religion": "Muslim", "has_rmd": False},
    {"id": "S1003", "name": "Rajendran s/o Muthu", "age": 58, "gender": "Male", "race": "Indian", "religion": "Hindu", "has_rmd": True},
    {"id": "S1004", "name": "Chloe de Souza", "age": 41, "gender": "Female", "race": "Eurasian", "religion": "Christian", "has_rmd": False},
    {"id": "S1005", "name": "Lim Boon Hock", "age": 84, "gender": "Male", "race": "Chinese", "religion": "Taoist", "has_rmd": False},
    {"id": "S1006", "name": "Fatimah Binte Ahmad", "age": 65, "gender": "Female", "race": "Malay", "religion": "Muslim", "has_rmd": True},
    {"id": "S1007", "name": "David Tan", "age": 35, "gender": "Male", "race": "Chinese", "religion": "Christian", "has_rmd": False},
    {"id": "S1008", "name": "Priya Devi", "age": 52, "gender": "Female", "race": "Indian", "religion": "Hindu", "has_rmd": True},
    {"id": "S1009", "name": "Jeremy Wong", "age": 47, "gender": "Male", "race": "Chinese", "religion": "Buddhist", "has_rmd": False},
    {"id": "S1010", "name": "Siti Aminah", "age": 78, "gender": "Female", "race": "Malay", "religion": "Muslim", "has_rmd": False}
]

rmd_conditions = ["Rheumatoid Arthritis", "Ankylosing Spondylitis", "Systemic Lupus Erythematosus", "Psoriatic Arthritis"]
general_conditions = ["Hypertension", "Type 2 Diabetes", "Hyperlipidemia", "Asthma", "Chronic Kidney Disease"]
rmd_meds = ["Methotrexate", "Sulfasalazine", "Hydroxychloroquine", "Etanercept", "Adalimumab"]
general_meds = ["Amlodipine", "Metformin", "Atorvastatin", "Salbutamol", "Lisinopril"]

nodes, edges, unique_entities = [], [], {}

def add_node(id, label, props):
    nodes.append({"id": id, "label": label, **props})

def add_edge(src, tgt, type, props=None):
    edges.append({"source": src, "target": tgt, "type": type, **(props or {})})

# 2. Process Data
for p in patients_data:
    pid = p['id']
    add_node(pid, "Patient", {"name": p['name'], "age": p['age'], "gender": p['gender']})
    
    # Demographics
    for label, val in [("Race", p['race']), ("Religion", p['religion']), ("AgeGroup", f"{(p['age'] // 10) * 10}s")]:
        eid = f"{label}_{val.replace(' ', '_')}"
        if eid not in unique_entities:
            add_node(eid, label, {"name": val})
            unique_entities[eid] = True
        add_edge(pid, eid, f"HAS_{label.upper()}")

    # Determine medical context
    p_conds = random.sample(general_conditions, 2)
    p_meds = random.sample(general_meds, 2)
    if p['has_rmd']:
        p_conds.append(random.choice(rmd_conditions))
        p_meds.append(random.choice(rmd_meds))

    # Link Patient DIRECTLY to Conditions/Medications
    for cond in p_conds:
        cid = f"Cond_{cond.replace(' ', '_')}"
        if cid not in unique_entities:
            add_node(cid, "Condition", {"name": cond, "is_rmd": cond in rmd_conditions})
            unique_entities[cid] = True
        # Edge represents frequency of mentions in clinical history
        add_edge(pid, cid, "DIAGNOSED_WITH", {"frequency": random.randint(5, 50)})
        
    for med in p_meds:
        mid = f"Med_{med.replace(' ', '_')}"
        if mid not in unique_entities:
            add_node(mid, "Medication", {"name": med})
            unique_entities[mid] = True
        add_edge(pid, mid, "PRESCRIBED", {"frequency": random.randint(10, 50)})

# 3. Save
pd.DataFrame(nodes).to_csv('kg_nodes_direct.csv', index=False)
pd.DataFrame(edges).to_csv('kg_edges_direct.csv', index=False)
print(f"Generated {len(nodes)} nodes and {len(edges)} direct edges.")