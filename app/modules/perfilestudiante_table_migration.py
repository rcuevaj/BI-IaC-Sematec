# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_perfiles_estudiante(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_usuario, edad, nivel_educativo, ocupacion
            FROM perfilestudiante;
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        perfiles = [dict(zip(columnas, fila)) for fila in resultados]
        print(f"📥 {len(perfiles)} perfiles de estudiante extraídos desde Supabase")
        return perfiles

    except Exception as e:
        print("❌ Error al extraer perfilestudiante desde Supabase:", e)
        return []

    finally:
        cursor.close()

# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_perfiles_estudiante_en_mysql(conn, perfiles):
    if not perfiles:
        print("⚠️ No hay perfiles de estudiante para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO perfilestudiante (id_usuario, edad, nivel_educativo, ocupacion)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            edad = VALUES(edad),
            nivel_educativo = VALUES(nivel_educativo),
            ocupacion = VALUES(ocupacion);
        """

        data = [
            (
                p['id_usuario'],
                p['edad'],
                p['nivel_educativo'],
                p['ocupacion']
            )
            for p in perfiles
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} perfiles de estudiante insertados o actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar perfilestudiante en MySQL:", e)

    finally:
        cursor.close()
