# simple-kg-/graph showcase
Contains synthetic patient and graph data, script for data generation and merging
Patient data:
- Structured: Demographic table
- Unstructured: ED/DS clinical notes
Graph Data:
- Nodes/Edges
- Master List




















# simple-kg-/graph generation
Folder structure 
simple-kg/
├── data/
│   └── SyntheticHSATestData/   <-- Patient data for LLM extraction
│   └── Placeholder/            <-- Placeholder folder
├── src/
│   ├── classes.py              <-- Node/Edge definitions
│   ├── job_creator.py          <-- Queue generator
│   └── chat.py                 <-- LLM extraction script
├── graph_outputs/              <-- Generated JSON fragments
└── jobs.csv                    <-- Generated Processing queue

Move files out of SyntheticHSATestData once whole job process is done


### Starting
Start venv: & '.\graph generation\src\venv\Scripts\activate'
Run job_creator.py to create jobs




### Ingesting to Neo4j
Patient graph fragments stored as JSON under graph_output folder

Pre-Ingestion Setup in Neo4j:
CREATE CONSTRAINT patient_id_unique IF NOT EXISTS FOR (p:Patient) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT med_id_unique IF NOT EXISTS FOR (m:Medication) REQUIRE m.id IS UNIQUE;
CREATE CONSTRAINT cond_id_unique IF NOT EXISTS FOR (c:Condition) REQUIRE c.id IS UNIQUE;