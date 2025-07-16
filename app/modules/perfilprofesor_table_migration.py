# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_perfiles_profesor(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_usuario, especialidad
            FROM perfilprofesor;
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        perfiles = [dict(zip(columnas, fila)) for fila in resultados]
        print(f"📥 {len(perfiles)} perfiles de profesor extraídos desde Supabase")
        return perfiles

    except Exception as e:
        print("❌ Error al extraer perfilprofesor desde Supabase:", e)
        return []

    finally:
        cursor.close()

# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_perfiles_profesor_en_mysql(conn, perfiles):
    if not perfiles:
        print("⚠️ No hay perfiles de profesor para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO perfilprofesor (id_usuario, especialidad)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE
            especialidad = VALUES(especialidad);
        """

        data = [(p['id_usuario'], p['especialidad']) for p in perfiles]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} perfiles insertados o actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar en MySQL:", e)

    finally:
        cursor.close()
