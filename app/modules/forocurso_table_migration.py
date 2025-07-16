# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_foro_curso_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_foro, id_curso, tema
            FROM forocurso;
        """)
        filas = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]
        foros = [dict(zip(columnas, fila)) for fila in filas]
        print(f"📥 {len(foros)} foros extraídos desde Supabase")
        return foros

    except Exception as e:
        print("❌ Error al extraer foros de curso:", e)
        return []

    finally:
        cursor.close()


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_foro_curso_en_mysql(conn, foros):
    if not foros:
        print("⚠️ No hay foros para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO forocurso (id_foro, id_curso, tema)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
            id_curso = VALUES(id_curso),
            tema     = VALUES(tema);
        """

        data = [(f["id_foro"], f["id_curso"], f["tema"]) for f in foros]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} foros insertados/actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar foros en MySQL:", e)

    finally:
        cursor.close()
