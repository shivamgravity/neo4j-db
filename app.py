from neo4j import GraphDatabase

# Connect to the database
uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j@123"))

# Function to create data
def create_data(tx):
    tx.run("CREATE (p:Person {name: 'Shivam'})")

# Run the function
with driver.session() as session:
    session.write_transaction(create_data)

driver.close()