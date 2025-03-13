def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_vectors (
        id SERIAL PRIMARY KEY,
        vector REAL[],  -- Storing the vector as an array
        source TEXT,
        title TEXT,
        page INT,
        chunk_id TEXT,
        doc_type TEXT
    );
    """)
    conn.commit()
    cursor.close()

# Call this function before inserting any data
conn = get_postgres_connection()
create_table_if_not_exists(conn)