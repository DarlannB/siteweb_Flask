import sqlite3

# Specify the database file path
database_file = "database.db"

# Read the SQL script content
with open("schema.sql", "r") as script_file:
    sql_script = script_file.read()

# Create a connection to the database
conn = sqlite3.connect(database_file)

# Execute the SQL script
cursor = conn.cursor()
cursor.executescript(sql_script)

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database created successfully.")
