import pandas as pd
import random

# 1. Configuration & Data Setup
patients_data = [
    {"id": "S1001", "name": "Tan Wei Ling", "age": 72, "gender": "Female", "race": "Chinese", "religion": "Buddhist", "has_rmd": True},
    {"id": "S1002", "name": "Muhammad Syazwan", "age": 29, "gender": "Male", "race": "Malay", "religion": "Muslim", "has_rmd": False},
    {"id": "S1003", "name": "Rajendran s/o Muthu", "age": 58, "gender": "Male", "race": "Indian", "religion": "Hindu", "has_rmd": True},
    {"id": "S1004", "name": "Chloe de Souza", "age": 41, "gender": "Female", "race": "Eurasian", "religion": "Christian", "has_rmd": False},
    {"id": "S1005", "name": "Lim Boon Hock", "age": 84, "gender": "Male", "race": "Chinese", "religion": "Taoist", "has_rmd": False}
]

# Medical Entities
rmd_conditions = ["Rheumatoid Arthritis", "Ankylosing Spondylitis", "Systemic Lupus Erythematosus", "Psoriatic Arthritis"]
general_conditions = ["Hypertension", "Type 2 Diabetes", "Hyperlipidemia", "Asthma", "Chronic Kidney Disease"]
rmd_meds = ["Methotrexate", "Sulfasalazine", "Hydroxychloroquine", "Etanercept", "Adalimumab"]
general_meds = ["Amlodipine", "Metformin", "Atorvastatin", "Salbutamol", "Lisinopril"]

# Templates
ed_complaints = ["Acute Joint Pain", "Fever", "Shortness of Breath", "Fall", "Chest Pain", "Giddiness"]
ds_outcomes = ["Stable for discharge", "Transferred to Community Hospital", "Follow-up at Specialist Clinic", "Home with medications"]

nodes = []
edges = []
unique_entities = {}

def add_node(id, label, properties):
    nodes.append({"id": id, "label": label, **properties})

def add_edge(source, target, edge_type):
    edges.append({"source": source, "target": target, "type": edge_type})

# 2. Generation Loop
for p in patients_data:
    pid = p['id']
    age_group = f"{(p['age'] // 10) * 10}s"
    
    # Patient Node
    add_node(pid, "Patient", {"name": p['name'], "age": p['age'], "gender": p['gender']})
    
    # Demographic Generalizations
    for label, val in [("Race", p['race']), ("Religion", p['religion']), ("AgeGroup", age_group)]:
        eid = f"{label}_{val.replace(' ', '_')}"
        if eid not in unique_entities:
            add_node(eid, label, {"name": val})
            unique_entities[eid] = True
        add_edge(pid, eid, f"HAS_{label.upper()}")

    # Assign Pre-existing Conditions and Meds
    p_conds = random.sample(general_conditions, 2)
    p_meds = random.sample(general_meds, 2)
    if p['has_rmd']:
        p_conds.append(random.choice(rmd_conditions))
        p_meds.append(random.choice(rmd_meds))

    # Link Patient to generalized Conditions/Meds
    for cond in p_conds:
        cid = f"Cond_{cond.replace(' ', '_')}"
        if cid not in unique_entities:
            add_node(cid, "Condition", {"name": cond, "is_rmd": cond in rmd_conditions})
            unique_entities[cid] = True
        add_edge(pid, cid, "HAS_CONDITION")
    for med in p_meds:
        mid = f"Med_{med.replace(' ', '_')}"
        if mid not in unique_entities:
            add_node(mid, "Medication", {"name": med})
            unique_entities[mid] = True
        add_edge(pid, mid, "TAKES_MEDICATION")

    # Generate 50 Notes
    for i in range(1, 26):
        # ED Note
        nid = f"Note_ED_{pid}_{i}"
        content = f"ED Visit {i}: Presents with {random.choice(ed_complaints)}. Hx: {', '.join(p_conds)}. Meds: {', '.join(p_meds)}."
        add_node(nid, "Note", {"type": "ED", "content": content})
        add_edge(pid, nid, "HAS_NOTE")
        
        # DS Note
        nid_ds = f"Note_DS_{pid}_{i}"
        content_ds = f"DS {i}: {random.choice(ds_outcomes)}. Managed {random.choice(p_conds)}."
        add_node(nid_ds, "Note", {"type": "DS", "content": content_ds})
        add_edge(pid, nid_ds, "HAS_NOTE")

# 3. Export to CSV
pd.DataFrame(nodes).to_csv('kg_nodes_rmd.csv', index=False)
pd.DataFrame(edges).to_csv('kg_edges_rmd.csv', index=False)
print("Files 'kg_nodes_rmd.csv' and 'kg_edges_rmd.csv' created.")