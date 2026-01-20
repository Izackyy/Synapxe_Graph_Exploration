import random

patients = [
    {"id": "S1001", "name": "Tan Wei Ling", "age": 72, "race": "Chinese"},
    {"id": "S1002", "name": "Muhammad Syazwan", "age": 29, "race": "Malay"},
    {"id": "S1003", "name": "Rajendran s/o Muthu", "age": 58, "race": "Indian"},
    {"id": "S1004", "name": "Chloe de Souza", "age": 41, "race": "Eurasian"},
    {"id": "S1005", "name": "Lim Boon Hock", "age": 84, "race": "Chinese"}
]

complaints = ["Chest Pain", "Shortness of Breath", "Abdominal Pain", "Fall", "Fever", "Giddiness"]
disposition = ["Discharged with 3 days MC", "Admitted to General Ward", "Referral to Specialist SOC", "Follow up at Polyclinic"]

with open("synthetic_patient_data.txt", "w") as f:
    f.write("=== SYNTHETIC SINGAPOREAN PATIENT DATASET ===\n\n")
    for p in patients:
        f.write(f"PATIENT: {p['name']} ({p['id']}) - Age: {p['age']}, Race: {p['race']}\n")
        f.write("-" * 50 + "\n")
        
        # Generate 25 ED Notes
        for i in range(1, 26):
            f.write(f"[ED Note {i}/25]\n")
            f.write(f"Complaint: {random.choice(complaints)}\n")
            f.write(f"Triage: P{random.randint(1,3)} | Vitals: BP {random.randint(100,160)}/{random.randint(60,95)} mmHg\n")
            f.write(f"Note: Patient presented with acute symptoms. {random.choice(disposition)}.\n\n")
        
        # Generate 25 Discharge Summaries
        for i in range(1, 26):
            f.write(f"[Discharge Summary {i}/25]\n")
            f.write(f"Diagnosis: Related to {random.choice(complaints)}\n")
            f.write("Hospital Course: Managed conservatively with IV fluids and monitoring. Condition stabilized.\n")
            f.write(f"Follow-up: {random.choice(disposition)}\n\n")
        
        f.write("=" * 60 + "\n\n")

print("File 'synthetic_patient_data.txt' has been generated with 250 notes.")
