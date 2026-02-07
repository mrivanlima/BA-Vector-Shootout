import os
import time
import json
import numpy as np
from faker import Faker
import pymssql
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
BATCH_SIZE = 100
VECTOR_DIM = 1536
SQL_PASSWORD = os.getenv("MSSQL_SA_PASSWORD") 
PG_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PG_DB = os.getenv("POSTGRES_DB", "vectordb")

fake = Faker()

def get_random_vector(dim):
    vec = np.random.rand(dim).astype(np.float32)
    vec /= np.linalg.norm(vec)
    return vec.tolist()

def setup_databases():
    print("--- SETTING UP DATABASES ---")
    
    # 1. SQL SERVER 2025 - Internal Host: 'sql2025' Port: 1433
    try:
        conn = pymssql.connect(server='sql2025', port=1433, user='sa', password=SQL_PASSWORD, autocommit=True, login_timeout=10)
        cursor = conn.cursor()
        cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'VectorDB') CREATE DATABASE VectorDB")
        cursor.execute("USE VectorDB")
        cursor.execute("""
            IF OBJECT_ID('ConsultingDocs', 'U') IS NULL
            CREATE TABLE ConsultingDocs (
                id INT IDENTITY(1,1) PRIMARY KEY,
                content NVARCHAR(MAX),
                embedding VECTOR(1536)
            )
        """)
        print("[SUCCESS] SQL 2025 (Native) ready.")
        conn.close()
    except Exception as e:
        print(f"[ERROR] SQL 2025 Setup Failed: {e}")

    # 2. SQL SERVER 2022 - Internal Host: 'sql2022' Port: 1433
    try:
        conn = pymssql.connect(server='sql2022', port=1433, user='sa', password=SQL_PASSWORD, autocommit=True, login_timeout=10)
        cursor = conn.cursor()
        cursor.execute("IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'VectorDB_Legacy') CREATE DATABASE VectorDB_Legacy")
        cursor.execute("USE VectorDB_Legacy")
        cursor.execute("""
            IF OBJECT_ID('ConsultingDocs', 'U') IS NULL
            CREATE TABLE ConsultingDocs (
                id INT IDENTITY(1,1) PRIMARY KEY,
                content NVARCHAR(MAX),
                embedding_json NVARCHAR(MAX) 
            )
        """)
        print("[SUCCESS] SQL 2022 (JSON) ready.")
        conn.close()
    except Exception as e:
        print(f"[ERROR] SQL 2022 Setup Failed: {e}")

    # 3. POSTGRES - Internal Host: 'postgres' Port: 5432
    try:
        conn = psycopg2.connect(host='postgres', port=5432, user='postgres', password=PG_PASSWORD, dbname=PG_DB, connect_timeout=10)
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consulting_docs (
                id SERIAL PRIMARY KEY,
                content TEXT,
                embedding vector(1536)
            )
        """)
        print("[SUCCESS] Postgres (pgvector) ready.")
        conn.close()
    except Exception as e:
        print(f"[ERROR] Postgres Setup Failed: {e}")

def run_load_test():
    print(f"\n--- STARTING LOAD TEST ({BATCH_SIZE} Records) ---")
    
    try:
        # Re-opening connections for the main loop
        conn_2025 = pymssql.connect(server='sql2025', port=1433, user='sa', password=SQL_PASSWORD, database='VectorDB', autocommit=True)
        conn_2022 = pymssql.connect(server='sql2022', port=1433, user='sa', password=SQL_PASSWORD, database='VectorDB_Legacy', autocommit=True)
        conn_pg = psycopg2.connect(host='postgres', port=5432, user='postgres', password=PG_PASSWORD, dbname=PG_DB)
        conn_pg.autocommit = True
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    cursor_2025 = conn_2025.cursor()
    cursor_2022 = conn_2022.cursor()
    cursor_pg = conn_pg.cursor()

    start_time = time.time()

    for i in range(BATCH_SIZE):
        doc_text = fake.paragraph(nb_sentences=3)
        vector_list = get_random_vector(VECTOR_DIM)
        vector_str = json.dumps(vector_list)

        # Batch inserts
        cursor_2025.execute("INSERT INTO ConsultingDocs (content, embedding) VALUES (%s, %s)", (doc_text, vector_str))
        cursor_2022.execute("INSERT INTO ConsultingDocs (content, embedding_json) VALUES (%s, %s)", (doc_text, vector_str))
        cursor_pg.execute("INSERT INTO consulting_docs (content, embedding) VALUES (%s, %s)", (doc_text, vector_list))

        if (i + 1) % 10 == 0:
            print(f"Inserted {i + 1}/{BATCH_SIZE} records...")

    end_time = time.time()
    print(f"\n--- LOAD COMPLETE in {end_time - start_time:.2f} seconds ---")
    
    conn_2025.close()
    conn_2022.close()
    conn_pg.close()

if __name__ == "__main__":
    setup_databases()
    run_load_test()