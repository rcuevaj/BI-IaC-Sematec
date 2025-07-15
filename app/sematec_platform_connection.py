import pymysql
import yaml
from encrypt_yml import decrypt

with open("credential.yml", "r") as f:
    config = yaml.safe_load(f)

# Fetch variables
USER = decrypt(config['app']['DBSematecPlataform']['user'])
PASSWORD = decrypt(config['app']['DBSematecPlataform']['password'])
HOST = decrypt(config['app']['DBSematecPlataform']['host'])
PORT = decrypt(config['app']['DBSematecPlataform']['port'])
DBNAME = decrypt(config['app']['DBSematecPlataform']['database'])

try:
    conn = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DBNAME,
        port=int(PORT)
    )

    with conn.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("✅ Conexión exitosa. Tablas disponibles:")
        for table in tables:
            print("-", table[0])

except pymysql.MySQLError as e:
    print("❌ Error de conexión:", e)

finally:
    if 'conn' in locals() and conn.open:
        conn.close()
