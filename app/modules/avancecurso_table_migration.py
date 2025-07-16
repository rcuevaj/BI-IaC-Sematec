# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_avances_curso_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_avance, id_inscripcion, modulo, porcentaje, fecha
            FROM avancecurso;
        """)
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        avances = [dict(zip(columnas, fila)) for fila in filas]
        print(f"📥 {len(avances)} registros de avancecurso extraídos desde Supabase")
        return avances

    except Exception as e:
        print("❌ Error al extraer avancecurso:", e)
        return []

    finally:
        cursor.close()


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_avances_curso_en_mysql(conn, avances):
    if not avances:
        print("⚠️ No hay avances para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO avancecurso (id_avance, id_inscripcion, modulo, porcentaje, fecha)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            id_inscripcion = VALUES(id_inscripcion),
            modulo         = VALUES(modulo),
            porcentaje     = VALUES(porcentaje),
            fecha          = VALUES(fecha);
        """

        data = [
            (
                a["id_avance"],
                a["id_inscripcion"],
                a["modulo"],
                a["porcentaje"],
                a["fecha"]
            )
            for a in avances
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} avances de curso insertados/actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar avances en MySQL:", e)

    finally:
        cursor.close()
