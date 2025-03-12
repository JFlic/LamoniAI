import psycopg2

try:
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="RaG32!happyL1fe",
        host="172.19.0.2",  # Try the container name or IP address
        port="5432"
    )
    print("Connected successfully!")
    conn.close()
except Exception as e:
    print(f"Connection failed: {e}")





# import psycopg2
# from psycopg2 import sql

# # Database connection details
# DB_NAME = "pgadmin"
# DB_USER = "postgres"
# DB_PASSWORD = "RaG32!happyL1fe"
# DB_HOST = "172.19.0.2"  # Change to your Docker container name if using Docker
# DB_PORT = "5432"

# # Connect to PostgreSQL
# def connect_db():
#     return psycopg2.connect(
#         dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
#     )

# # Create a table if it doesn't exist
# def create_table():
#     conn = connect_db()
#     cursor = conn.cursor()
#     cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
#     cursor.execute(
#         """
#         CREATE TABLE IF NOT EXISTS dummy_data (
#             id SERIAL PRIMARY KEY,
#             name TEXT NOT NULL,
#             age INT NOT NULL,
#             city TEXT NOT NULL,
#             embedding vector(3) -- Adjust dimension as needed
#         );
#         """
#     )
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("Table with vector column created successfully.")

# # Insert dummy data with vector
# def insert_dummy_data():
#     conn = connect_db()
#     cursor = conn.cursor()
#     dummy_records = [
#         ("Alice", 25, "New York", [0.1, 0.2, 0.3]),
#         ("Bob", 30, "Los Angeles", [0.4, 0.5, 0.6]),
#         ("Charlie", 28, "Chicago", [0.7, 0.8, 0.9]),
#         ("David", 35, "Houston", [0.2, 0.3, 0.5]),
#         ("Emma", 22, "Miami", [0.9, 0.1, 0.4]),
#     ]
#     insert_query = "INSERT INTO dummy_data (name, age, city, embedding) VALUES (%s, %s, %s, %s);"
#     cursor.executemany(insert_query, dummy_records)
#     conn.commit()
#     cursor.close()
#     conn.close()
#     print("Dummy data with vectors inserted successfully.")

# if __name__ == "__main__":
#     create_table()
#     insert_dummy_data()
