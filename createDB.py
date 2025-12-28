import psycopg2

POSTGRES_PASSWORD = "12345678"

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = POSTGRES_PASSWORD,
    host = "localhost",
    port = "5432"
)
conn.autocommit = True
cur = conn.cursor()


try:
    cur.execute("CREATE DATABASE archaeology;")
    print("Database archaeology created.")
except Exception as e:
    print("Database already exists or error:", e)
    
    
try:
    cur.execute("CREATE USER s WITH PASSWORD '12345678';")
    print("User 's' created")
except Exception as e:
    print("User already exists or error:", e)
    

try:
    cur.execute("GRANT ALL PRIVILEGES ON DATABASE archaeology TO s;")
    print("Privileges granted to 's'")
except Exception as e:
    print("Error granting privileges:", e)
    
    
cur.close()
conn.close()