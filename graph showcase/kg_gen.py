import pandas as pd
import random

# 1. Setup Patient Personas (10 Patients)
patients_data = [
    {"id": "S1001", "name": "Tan Wei Ling", "age": 72, "gender": "Female", "race": "Chinese", "religion": "Buddhist", "has_rdm": True},
    {"id": "S1002", "name": "Muhammad Syazwan", "age": 29, "gender": "Male", "race": "Malay", "religion": "Muslim", "has_rdm": False},
    {"id": "S1003", "name": "Rajendran s/o Muthu", "age": 58, "gender": "Male", "race": "Indian", "religion": "Hindu", "has_rdm": True},
    {"id": "S1004", "name": "Chloe de Souza", "age": 41, "gender": "Female", "race": "Eurasian", "religion": "Christian", "has_rdm": False},
    {"id": "S1005", "name": "Lim Boon Hock", "age": 84, "gender": "Male", "race": "Chinese", "religion": "Taoist", "has_rdm": False},
    {"id": "S1006", "name": "Fatimah Binte Ahmad", "age": 65, "gender": "Female", "race": "Malay", "religion": "Muslim", "has_rdm": True},
    {"id": "S1007", "name": "David Tan", "age": 35, "gender": "Male", "race": "Chinese", "religion": "Christian", "has_rdm": False},
    {"id": "S1008", "name": "Priya Devi", "age": 52, "gender": "Female", "race": "Indian", "religion": "Hindu", "has_rdm": True},
    {"id": "S1009", "name": "Jeremy Wong", "age": 47, "gender": "Male", "race": "Chinese", "religion": "Buddhist", "has_rdm": False},
    {"id": "S1010", "name": "Siti Aminah", "age": 78, "gender": "Female", "race": "Malay", "religion": "Muslim", "has_rdm": False}
]

# Assets for Complexity
medical_conditions = ["Hypertension", "Type 2 Diabetes", "Hyperlipidemia", "Chronic Kidney Disease", "Atrial Fibrillation", "Obesity"]
drugs = ["Atorvastatin", "Lisinopril", "Metformin", "Amlodipine", "Warfarin", "Hydrochlorothiazide", "Aspirin"]
rdm_triggers = ["Statin-Induced Myopathy", "Crush Injury", "Extreme Physical Exertion", "Prolonged Immobilization"]

nodes, edges = [], []
unique_entities = set()

def add_node(node_id, label, props):
    if node_id not in unique_entities:
        nodes.append({"id": node_id, "label": label, **props})
        unique_entities.add(node_id)

def add_edge(src, tgt, edge_type, props=None):
    edges.append({"source": src, "target": tgt, "type": edge_type, **(props or {})})

# --- 2. GENERATE GLOBAL HUB ---
add_node("Condition_RDM", "Condition", {"name": "Rhabdomyolysis"})

# --- 3. GENERATE PATIENT ECOSYSTEMS ---
for p in patients_data:
    pid = p['id']
    add_node(pid, "Patient", {"name": p['name'], "age": p['age'], "gender": p['gender']})
    
    # Demographic Nodes & Edges
    for label, val in [("Race", p['race']), ("Religion", p['religion']), ("AgeGroup", f"{(p['age'] // 10) * 10}s")]:
        eid = f"{label}_{val.replace(' ', '_')}"
        add_node(eid, label, {"name": val})
        add_edge(pid, eid, f"HAS_{label.upper()}")

    # Concurrent Conditions (1-3)
    p_conds = random.sample(medical_conditions, random.randint(1, 3))
    for cond in p_conds:
        cid = f"Cond_{cond.replace(' ', '_')}"
        add_node(cid, "Condition", {"name": cond})
        add_edge(pid, cid, "HAS_HISTORY")

    # Drug Combinations (2-4)
    p_drugs = random.sample(drugs, random.randint(2, 4))
    for drug in p_drugs:
        did = f"Drug_{drug.replace(' ', '_')}"
        add_node(did, "Medication", {"name": drug})
        add_edge(pid, did, "PRESCRIBED")

    # RDM Path (The Global Hub Connections)
    if p['has_rdm']:
        # S1001 and S1003 share the Statin Trigger
        trigger = "Statin-Induced Myopathy" if pid in ["S1001", "S1003"] else random.choice(rdm_triggers[1:])
        tid = f"Trigger_{trigger.replace(' ', '_')}"
        add_node(tid, "Trigger", {"name": trigger})
        
        # Connect Trigger to Hub
        add_edge(tid, "Condition_RDM", "CAUSES")
        
        # Connect Patient to Hub (Carrying Note Summary Data)
        # We store the aggregate results of the 20 emergency/discharge notes here
        add_edge(pid, "Condition_RDM", "DIAGNOSED_WITH", {
            "peak_ck_from_er": random.randint(15000, 50000),
            "discharge_ck": random.randint(200, 900),
            "er_notes_count": 10,
            "ds_notes_count": 10
        })
        add_edge(pid, tid, "TRIGGERED_BY")

# --- 4. EXPORT ---
pd.DataFrame(nodes).to_csv('nodes_4con3drug.csv', index=False)
pd.DataFrame(edges).to_csv('edges_4con3drug.csv', index=False)

# Create Joined Reference Table
nodes_df = pd.DataFrame(nodes)
edges_df = pd.DataFrame(edges)
name_map = nodes_df.set_index('id')['name'].to_dict()
joined_df = edges_df.copy()
joined_df['source_name'] = joined_df['source'].map(name_map)
joined_df['target_name'] = joined_df['target'].map(name_map)
joined_df.to_csv('edges_nodes_4con3drug.csv', index=False)

print("CSVs Generated: nodes_4con3drug.csv, edges_4con3drug.csv, and edges_nodes_4con3drug.csv")