import random
from datetime import datetime, timedelta

# 1. Setup V3 Specific Patient Data
# Mapping of IDs to Names and their V3 Clinical Status for logic-based note generation
v3_patients = {
    "S1011": {"name": "Rajendran s/o Muthu", "status": "INDEX_CASE"},
    "S1012": {"name": "Tan Wei Ling", "status": "CRITICAL_SURVIVOR"},
    "S1013": {"name": "Priya Devi", "status": "DIAGNOSED_CASE"},
    "S1014": {"name": "Chloe de Souza", "status": "CLINICAL_TWIN"},
    "S1015": {"name": "David Lim", "status": "CLINICAL_TWIN"},
    "S1016": {"name": "Mei Xin", "status": "CLINICAL_TWIN"},
    "S1017": {"name": "Fatimah Binte Ahmad", "status": "CLINICAL_TWIN"},
    "S1018": {"name": "Muhammad Syazwan", "status": "CLINICAL_TWIN"},
    "S1019": {"name": "Siti Aminah", "status": "CLINICAL_TWIN"},
    "S1020": {"name": "Karthik Raja", "status": "CLINICAL_TWIN"},
    "S1021": {"name": "Patient_11", "status": "CLINICAL_TWIN"}
}

symptoms = ["severe myalgia", "tea-colored urine", "bilateral thigh weakness", "generalized fatigue", "muscle tenderness"]
medications = ["Atorvastatin", "Metformin", "Lisinopril", "Amlodipine", "Aspirin", "Warfarin"]
outcomes = ["CK levels trending down", "Renal function stable", "Hyperkalemia resolved", "Hydration maintained"]

def get_random_date(start_year=2024, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def generate_v3_notes_txt(filename="v3_clinical_notes.txt"):
    with open(filename, "w") as f:
        for pid, pdata in v3_patients.items():
            f.write(f"========================================\n")
            f.write(f"PATIENT RECORD: {pid} - {pdata['name']}\n")
            f.write(f"========================================\n\n")
            
            episode_start = get_random_date()
            
            # Generating 10 sequences for Emergency Department and 10 for Discharge Summary
            for n_type in ["EMERGENCY DEPARTMENT", "DISCHARGE SUMMARY"]:
                for i in range(1, 11):
                    # Temporal logic: ED notes within 24h, Discharge 3-10 days later
                    if n_type == "EMERGENCY DEPARTMENT":
                        note_date = episode_start + timedelta(hours=random.randint(0, 24))
                        # Lab logic based on V3 risk status
                        if pdata['status'] in ["INDEX_CASE", "DIAGNOSED_CASE"]:
                            ck_level = random.randint(25000, 48000)
                        elif pdata['status'] == "CRITICAL_SURVIVOR":
                            ck_level = random.randint(900, 2200)
                        else:
                            ck_level = random.randint(100, 250)
                    else:
                        note_date = episode_start + timedelta(days=random.randint(3, 10))
                        ck_level = random.randint(150, 980)
                    
                    # DDI pattern enforcement for high-risk patients
                    if pdata['status'] in ["INDEX_CASE", "CRITICAL_SURVIVOR"]:
                        current_meds = ["Lisinopril", "Atorvastatin"] + random.sample(["Metformin", "Amlodipine", "Aspirin"], 1)
                    else:
                        current_meds = random.sample(medications, random.randint(2, 4))
                    
                    f.write(f"Note ID: {n_type[0:2].replace(' ', '')}_{pid}_{i}\n")
                    f.write(f"Date: {note_date.strftime('%Y-%m-%d %H:%M')}\n")
                    f.write(f"Type: {n_type} (Sequence: {i})\n")
                    f.write(f"Concurrent Meds: {', '.join(current_meds)}\n")
                    
                    if n_type == "EMERGENCY DEPARTMENT":
                        # Clinical twins receive baseline presentation notes
                        pres = random.choice(symptoms) if pdata['status'] != "CLINICAL_TWIN" else "generalized fatigue"
                        f.write(f"Clinical Presentation: Patient presents with {pres}.\n")
                        f.write(f"Initial Lab: Creatine Kinase (CK) recorded at {ck_level} U/L.\n")
                    else:
                        f.write(f"Recovery Status: {random.choice(outcomes)}.\n")
                        f.write(f"Discharge Lab: CK improved to {ck_level} U/L.\n")
                    
                    f.write("-" * 20 + "\n")
            f.write("\n")

    print(f"Successfully generated V3 records for 11 patients in {filename}")

if __name__ == "__main__":
    generate_v3_notes_txt()