# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_resultados_evaluacion_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_resultado, id_evaluacion, id_usuario, puntaje
            FROM resultadoevaluacion;
        """)
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        resultados = [dict(zip(columnas, fila)) for fila in filas]
        print(f"📥 {len(resultados)} resultados de evaluación extraídos desde Supabase")
        return resultados

    except Exception as e:
        print("❌ Error al extraer resultados de evaluación:", e)
        return []

    finally:
        cursor.close()


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_resultados_evaluacion_en_mysql(conn, resultados):
    if not resultados:
        print("⚠️ No hay resultados para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO resultadoevaluacion (id_resultado, id_evaluacion, id_usuario, puntaje)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            id_evaluacion = VALUES(id_evaluacion),
            id_usuario    = VALUES(id_usuario),
            puntaje       = VALUES(puntaje);
        """

        data = [
            (
                r["id_resultado"],
                r["id_evaluacion"],
                r["id_usuario"],
                r["puntaje"]
            )
            for r in resultados
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} resultados insertados/actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar resultados de evaluación en MySQL:", e)

    finally:
        cursor.close()
