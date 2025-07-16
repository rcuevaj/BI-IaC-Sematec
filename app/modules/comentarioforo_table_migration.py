# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_comentarios_foro_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_comentario, id_foro, id_usuario, mensaje, fecha
            FROM comentarioforo;
        """)
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        comentarios = [dict(zip(columnas, fila)) for fila in filas]
        print(f"📥 {len(comentarios)} comentarios extraídos desde Supabase")
        return comentarios

    except Exception as e:
        print("❌ Error al extraer comentarios del foro:", e)
        return []

    finally:
        cursor.close()


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_comentarios_foro_en_mysql(conn, comentarios):
    if not comentarios:
        print("⚠️ No hay comentarios para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO comentarioforo (id_comentario, id_foro, id_usuario, mensaje, fecha)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            id_foro    = VALUES(id_foro),
            id_usuario = VALUES(id_usuario),
            mensaje    = VALUES(mensaje),
            fecha      = VALUES(fecha);
        """

        data = [
            (
                c["id_comentario"],
                c["id_foro"],
                c["id_usuario"],
                c["mensaje"],
                c["fecha"]
            )
            for c in comentarios
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} comentarios insertados/actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar comentarios en MySQL:", e)

    finally:
        cursor.close()
