import pandas as pd
import random
from datetime import datetime, timedelta

# 1. Load Version 1 Data
# Ensure these files are in your working directory
nodes_v1 = pd.read_csv('nodes_4con3drug.csv')
edges_v1 = pd.read_csv('edges_4con3drug.csv')

def get_random_date(start_year=2018, end_year=2025):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

# Dictionary to store patient-specific base dates for consistency
patient_dates = {}
patients = nodes_v1[nodes_v1['label'] == 'Patient']['id'].unique()

for pid in patients:
    start_dt = get_random_date()
    los = random.randint(3, 14) # Length of stay: 3 to 14 days
    end_dt = start_dt + timedelta(days=los)
    patient_dates[pid] = {'start': start_dt, 'end': end_dt, 'los': los}

# 2. Update Nodes with Time Attributes
nodes_with_time = nodes_v1.copy()
nodes_with_time['start_date'] = None
nodes_with_time['end_date'] = None

for idx, row in nodes_with_time.iterrows():
    if row['id'] in patient_dates:
        nodes_with_time.at[idx, 'start_date'] = patient_dates[row['id']]['start'].strftime('%Y-%m-%d')
        nodes_with_time.at[idx, 'end_date'] = patient_dates[row['id']]['end'].strftime('%Y-%m-%d')

# 3. Update Edges with Time Attributes and Durations
edges_with_time = edges_v1.copy()
edges_with_time['start_date'] = None
edges_with_time['end_date'] = None
edges_with_time['duration_days'] = None
edges_with_time['occurrence_date'] = None

for idx, row in edges_with_time.iterrows():
    pid = row['source']
    rel_type = row['type']
    
    if pid in patient_dates:
        p_info = patient_dates[pid]
        
        if rel_type == 'DIAGNOSED_WITH':
            edges_with_time.at[idx, 'occurrence_date'] = p_info['start'].strftime('%Y-%m-%d')
            edges_with_time.at[idx, 'duration_days'] = p_info['los']
            edges_with_time.at[idx, 'start_date'] = p_info['start'].strftime('%Y-%m-%d')
            edges_with_time.at[idx, 'end_date'] = p_info['end'].strftime('%Y-%m-%d')
            
        elif rel_type == 'PRESCRIBED':
            m_start = p_info['start'] - timedelta(days=random.randint(0, 60))
            m_dur = random.randint(30, 365)
            m_end = m_start + timedelta(days=m_dur)
            edges_with_time.at[idx, 'start_date'] = m_start.strftime('%Y-%m-%d')
            edges_with_time.at[idx, 'end_date'] = m_end.strftime('%Y-%m-%d')
            edges_with_time.at[idx, 'duration_days'] = m_dur
            edges_with_time.at[idx, 'occurrence_date'] = m_start.strftime('%Y-%m-%d')
            
        elif rel_type == 'HAS_HISTORY':
            h_occ = p_info['start'] - timedelta(days=random.randint(180, 1000))
            edges_with_time.at[idx, 'occurrence_date'] = h_occ.strftime('%Y-%m-%d')
            
        elif rel_type == 'TRIGGERED_BY':
            t_occ = p_info['start'] - timedelta(hours=random.randint(1, 48))
            edges_with_time.at[idx, 'occurrence_date'] = t_occ.strftime('%Y-%m-%d')

# 4. Generate Reference Table (Joined for your review)
ref_table = edges_with_time.merge(nodes_v1[['id', 'name', 'age', 'gender']], left_on='source', right_on='id', how='left')
ref_table = ref_table.rename(columns={'name': 'source_name'}).drop(columns=['id'])
ref_table = ref_table.merge(nodes_v1[['id', 'name']], left_on='target', right_on='id', how='left')
ref_table = ref_table.rename(columns={'name': 'target_name'}).drop(columns=['id'])

# 5. Save files
nodes_with_time.to_csv('nodes_with_time.csv', index=False)
edges_with_time.to_csv('edges_with_time.csv', index=False)
ref_table.to_csv('edges_nodes_with_time.csv', index=False)

