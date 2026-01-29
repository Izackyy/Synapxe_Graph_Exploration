import pandas as pd

def generate_updated_demographic(nodes_file='nodes_v3.csv', demo_file='demographic.csv'):
    # Load the source files
    nodes_v3 = pd.read_csv(nodes_file)
    demographic = pd.read_csv(demo_file)

    # 1. Extract only Patient nodes from the v3 dataset
    v3_patients = nodes_v3[nodes_v3['label'] == 'Patient'].copy()

    # 2. Map v3 columns to match the demographic.csv schema
    # v3: ['id', 'name', 'age', 'gender', 'ethnicity', 'religion']
    # demographic: ['Patient ID', 'Name', 'Age', 'Gender', 'Race', 'Religion', 'Housing Type']
    v3_mapped = v3_patients[['id', 'name', 'age', 'gender', 'ethnicity', 'religion']].copy()
    v3_mapped.columns = ['Patient ID', 'Name', 'Age', 'Gender', 'Race', 'Religion']

    # 3. Merge with existing demographic info to retain 'Housing Type' for known patients
    # We merge on 'Name' to bridge the different ID formats (e.g., S1001 vs P01)
    merged = v3_mapped.merge(demographic[['Name', 'Housing Type']], on='Name', how='left')

    # 4. Include any patients that were in the original demographic but not in nodes_v3
    only_in_orig = demographic[~demographic['Name'].isin(v3_mapped['Name'])]
    final_demographic = pd.concat([merged, only_in_orig], ignore_index=True)

    # 5. Clean up: Sort by Patient ID and reset index
    final_demographic = final_demographic.sort_values(by='Patient ID').reset_index(drop=True)

    # 6. Save the final updated table
    output_filename = 'updated_demographic_v3.csv'
    final_demographic.to_csv(output_filename, index=False)
    
    print(f"Successfully generated {len(final_demographic)} patient records in {output_filename}")
    return final_demographic

if __name__ == "__main__":
    generate_updated_demographic()