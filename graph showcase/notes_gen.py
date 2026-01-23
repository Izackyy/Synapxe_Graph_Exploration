import random
from datetime import datetime, timedelta

# 1. Setup Data
patient_ids = [f"S10{str(i).zfill(2)}" for i in range(1, 11)]
symptoms = ["severe myalgia", "tea-colored urine", "bilateral thigh weakness", "generalized fatigue", "muscle tenderness"]
medications = ["Atorvastatin", "Metformin", "Lisinopril", "Amlodipine", "Aspirin", "Warfarin"]
outcomes = ["CK levels trending down", "Renal function stable", "Hyperkalemia resolved", "Hydration maintained"]

def get_random_date(start_year=2018, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def generate_notes_txt(filename="rdm_clinical_notes.txt"):
    with open(filename, "w") as f:
        for pid in patient_ids:
            f.write(f"========================================\n")
            f.write(f"PATIENT RECORD: {pid}\n")
            f.write(f"========================================\n\n")
            
            # Generate a base date for this specific clinical episode
            episode_start = get_random_date()
            
            for n_type in ["EMERGENCY DISCHARGE", "DISCHARGE SUMMARY"]:
                for i in range(1, 11):
                    # Logical Date Progression: 
                    # ER notes happen within 24h of episode start.
                    # Discharge notes happen 3-10 days later.
                    if "EMERGENCY" in n_type:
                        note_date = episode_start + timedelta(hours=random.randint(0, 24))
                    else:
                        note_date = episode_start + timedelta(days=random.randint(3, 10))
                    
                    ck_level = random.randint(5000, 45000)
                    current_meds = random.sample(medications, random.randint(2, 4))
                    
                    f.write(f"Note ID: {n_type[:2]}_{pid}_{i}\n")
                    f.write(f"Date: {note_date.strftime('%Y-%m-%d %H:%M')}\n") # Added Date Line
                    f.write(f"Type: {n_type} (Sequence: {i})\n")
                    f.write(f"Concurrent Meds: {', '.join(current_meds)}\n")
                    
                    if "EMERGENCY" in n_type:
                        f.write(f"Clinical Presentation: Patient presents with {random.choice(symptoms)}.\n")
                        f.write(f"Initial Lab: Creatine Kinase (CK) recorded at {ck_level} U/L.\n")
                    else:
                        f.write(f"Recovery Status: {random.choice(outcomes)}.\n")
                        f.write(f"Discharge Lab: CK improved to {random.randint(200, 1000)} U/L.\n")
                    
                    f.write("-" * 20 + "\n")
            f.write("\n")

    print(f"Successfully generated 200 notes with dates in {filename}")

if __name__ == "__main__":
    generate_notes_txt()