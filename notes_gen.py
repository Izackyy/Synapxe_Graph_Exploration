import random

# 1. Setup Data
patient_ids = [f"S10{str(i).zfill(2)}" for i in range(1, 11)]
symptoms = ["severe myalgia", "tea-colored urine", "bilateral thigh weakness", "generalized fatigue", "muscle tenderness"]
medications = ["Atorvastatin", "Metformin", "Lisinopril", "Amlodipine", "Aspirin", "Warfarin"]
outcomes = ["CK levels trending down", "Renal function stable", "Hyperkalemia resolved", "Hydration maintained"]

def generate_notes_txt(filename="rdm_clinical_notes.txt"):
    with open(filename, "w") as f:
        for pid in patient_ids:
            f.write(f"========================================\n")
            f.write(f"PATIENT RECORD: {pid}\n")
            f.write(f"========================================\n\n")
            
            # Generate 10 Emergency and 10 Discharge Notes
            for n_type in ["EMERGENCY DISCHARGE", "DISCHARGE SUMMARY"]:
                for i in range(1, 11):
                    ck_level = random.randint(5000, 45000)
                    current_meds = random.sample(medications, random.randint(2, 4))
                    
                    f.write(f"Note ID: {n_type[:2]}_{pid}_{i}\n")
                    f.write(f"Type: {n_type} (Sequence: {i})\n")
                    f.write(f"Concurrent Meds: {', '.join(current_meds)}\n")
                    
                    if "EMERGENCY" in n_type:
                        f.write(f"Clinical Presentation: Patient presents with {random.choice(symptoms)}.\n")
                        f.write(f"Initial Lab: Creatine Kinase (CK) recorded at {ck_level} U/L.\n")
                    else:
                        f.write(f"Recovery Status: {random.choice(outcomes)}.\n")
                        f.write(f"Discharge Lab: CK improved to {random.randint(200, 1000)} U/L.\n")
                    
                    f.write("-" * 20 + "\n")
            f.write("\n") # Space between patients

    print(f"Successfully generated 200 notes in {filename}")

if __name__ == "__main__":
    generate_notes_txt()