import psycopg2
import yaml
from encrypt_yml import decrypt

with open("credential.yml", "r") as f:
    config = yaml.safe_load(f)

# Fetch variables
USER = decrypt(config['app']['db']['user'])
PASSWORD = decrypt(config['app']['db']['password'])
HOST = decrypt(config['app']['db']['host'])
PORT = decrypt(config['app']['db']['port'])
DBNAME = decrypt(config['app']['db']['name'])

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")

    # Create a cursor to execute SQL queries
    cursor = connection.cursor()

    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")