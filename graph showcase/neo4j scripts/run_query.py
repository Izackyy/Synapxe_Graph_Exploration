
# %% Connection details from Neo4j Aura
from neo4j import GraphDatabase
import os

uri = "neo4j+s://e951a015.databases.neo4j.io"
username = "neo4j"
password = "8nHfqS01x9Zao0LLYD9-Yev4gIVUbQO4lnSvXqLJcDE"
database = "neo4j"

# Create driver and run query
driver = GraphDatabase.driver(uri, auth=(username, password))

try:
    with driver.session(database=database) as session:
        result = session.run("MATCH (n) RETURN count(n)")
        for record in result:
            print(f"Total nodes in database: {record[0]}")
finally:
    driver.close()


# %% create kg
