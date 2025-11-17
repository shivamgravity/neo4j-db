from neo4j import GraphDatabase

# Connect to the database
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

class MovieApp:
    def __init__(self, uri, auth):
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def close(self):
        self.driver.close()
    
    # this is the function to create data - nodes and relationships
    def create_movie_data(self):
        with self.driver.session() as session:
            query = """
                CREATE (keanu:Person {name: 'Keanu Reeves', born: 1964})
                CREATE (matrix:Movie {title: 'The Matrix', released: 1999})
                CREATE (john:Person {name: 'John Wick', born: 1964})
                CREATE (wick_movie:Movie {title: 'John Wick', released: 2014})

                CREATE (keanu)-[:ACTED_IN {role: 'Neo'}]->(matrix)
                CREATE (keanu)-[:ACTED_IN {role: 'John Wick'}]->(wick_movie)
                """
            session.run(query)
            print("Data created successfully!")
    
    # this is the function to read the data - like find movies a person acted in.
    def find_movies_by_actor(self, actor_name):
        with self.driver.session() as session:
            query = """
                MATCH (p:Person {name: $name})-[:ACTED_IN]->(m:Movie)
                RETURN m.title as title, m.released as released
                """
            result = session.run(query, name=actor_name)

            print(f"\nMovies starring {actor_name}:")
            movies = [record for record in result]
            if not movies:
                print("No movies found.")
            for record in movies:
                print(f"- {record['title']} ({record['released']})")
    
    # this is the function to delete a data
    def clean_database(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("Database cleared!")
    
if __name__ == "__main__":
    app = MovieApp(URI, AUTH)

    try:
        app.clean_database()
        app.create_movie_data()
        app.find_movies_by_actor("Keanu Reeves")
    finally:
        app.close()
