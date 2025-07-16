# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_cursos_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_curso, nombre, descripcion, categoria, nivel, id_profesor
            FROM curso;
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        cursos = [dict(zip(columnas, fila)) for fila in resultados]
        print(f"📥 {len(cursos)} cursos extraídos desde Supabase")
        return cursos

    except Exception as e:
        print("❌ Error al extraer cursos desde Supabase:", e)
        return []

    finally:
        cursor.close()

# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_cursos_en_mysql(conn, cursos):
    if not cursos:
        print("⚠️ No hay cursos para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO curso (id_curso, nombre, descripcion, categoria, nivel, id_profesor)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            descripcion = VALUES(descripcion),
            categoria = VALUES(categoria),
            nivel = VALUES(nivel),
            id_profesor = VALUES(id_profesor);
        """

        data = [
            (
                c['id_curso'],
                c['nombre'],
                c['descripcion'],
                c['categoria'],
                c['nivel'],
                c['id_profesor']
            )
            for c in cursos
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} cursos insertados o actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar cursos en MySQL:", e)

    finally:
        cursor.close()
