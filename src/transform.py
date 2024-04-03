import psycopg
import os

# Database connection parameters (replaced with environment variables)
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

# Function to execute SQL script
def execute_sql_script(script_path):
    try:
        # Connect to the database
        conn = psycopg.connect(
            dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
        )
        cursor = conn.cursor()

        # Read SQL script
        with open(script_path, "r") as sql_file:
            sql_script = sql_file.read()

        # Execute SQL script
        cursor.execute(sql_script)
        conn.commit()
        print(f"Successfully executed SQL script: {script_path}")

    except (Exception, psycopg.DatabaseError) as error:
        print(f"Error executing SQL script {script_path}: {error}")

    finally:
        # Close database connection
        if conn is not None:
            cursor.close()
            conn.close()


# Directory containing SQL scripts
sql_dir = "sql"

# List all SQL files in the directory
sql_files = sorted(os.listdir(sql_dir))

# Execute SQL files for creating/populating tables
for filename in sql_files:
    if filename.startswith("create") or filename.startswith("populate"):
        script_path = os.path.join(sql_dir, filename)
        execute_sql_script(script_path)

# Execute SQL files for transformations
for filename in sql_files:
    if not filename.startswith("create") and not filename.startswith("populate"):
        script_path = os.path.join(sql_dir, filename)
        execute_sql_script(script_path)
