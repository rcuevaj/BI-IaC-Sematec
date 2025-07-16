# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_inscripciones_desde_supabase(conn):
    """Extrae todas las inscripciones desde Supabase (PostgreSQL)."""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_inscripcion,
                   id_usuario,
                   id_curso,
                   fecha_inscripcion,
                   estado
            FROM inscripcion;
        """)
        filas = cursor.fetchall()
        columnas = [d[0] for d in cursor.description]
        inscripciones = [dict(zip(columnas, fila)) for fila in filas]
        print(f"📥 {len(inscripciones)} inscripciones extraídas desde Supabase")
        return inscripciones

    except Exception as e:
        print("❌ Error al extraer inscripciones:", e)
        return []

    finally:
        cursor.close()


# ====================================
# 🔄 ETAPA: Transformación
# Normaliza `estado` a minúsculas y sin espacios.
# ====================================

def transformar_inscripciones(raw):
    for r in raw:
        r["estado"] = r["estado"].strip().lower()
    print("🧽 Transformación de inscripciones completada")
    return raw


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_inscripciones_en_mysql(conn, inscripciones):
    """Inserta o actualiza inscripciones en MySQL RDS."""
    if not inscripciones:
        print("⚠️ No hay inscripciones para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_q = """
        INSERT INTO inscripcion
            (id_inscripcion, id_usuario, id_curso, fecha_inscripcion, estado)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            id_usuario        = VALUES(id_usuario),
            id_curso          = VALUES(id_curso),
            fecha_inscripcion = VALUES(fecha_inscripcion),
            estado            = VALUES(estado);
        """

        data = [
            (
                i["id_inscripcion"],
                i["id_usuario"],
                i["id_curso"],
                i["fecha_inscripcion"],
                i["estado"]
            )
            for i in inscripciones
        ]

        cursor.executemany(insert_q, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} inscripciones insertadas/actualizadas en MySQL")

    except Exception as e:
        print("❌ Error al insertar inscripciones en MySQL:", e)

    finally:
        cursor.close()
