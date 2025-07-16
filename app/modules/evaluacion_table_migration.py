# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_evaluaciones_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_evaluacion, id_curso, titulo, fecha
            FROM evaluacion;
        """)
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        evaluaciones = [dict(zip(columnas, fila)) for fila in filas]
        print(f"📥 {len(evaluaciones)} evaluaciones extraídas desde Supabase")
        return evaluaciones

    except Exception as e:
        print("❌ Error al extraer evaluaciones:", e)
        return []

    finally:
        cursor.close()


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_evaluaciones_en_mysql(conn, evaluaciones):
    if not evaluaciones:
        print("⚠️ No hay evaluaciones para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO evaluacion (id_evaluacion, id_curso, titulo, fecha)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            id_curso = VALUES(id_curso),
            titulo   = VALUES(titulo),
            fecha    = VALUES(fecha);
        """

        data = [
            (
                e["id_evaluacion"],
                e["id_curso"],
                e["titulo"],
                e["fecha"]
            )
            for e in evaluaciones
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} evaluaciones insertadas/actualizadas en MySQL")

    except Exception as e:
        print("❌ Error al insertar evaluaciones en MySQL:", e)

    finally:
        cursor.close()
