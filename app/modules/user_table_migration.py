# ====================================
# 🔍 ETAPA: Extracción desde Supabase
# ====================================

def extraer_usuarios_desde_supabase(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id_usuario, nombre, apellido, correo, contraseña, rol
            FROM usuario;
        """)
        resultados = cursor.fetchall()
        columnas = [desc[0] for desc in cursor.description]

        usuarios = [dict(zip(columnas, fila)) for fila in resultados]
        print(f"📥 {len(usuarios)} usuarios extraídos desde Supabase")
        return usuarios

    except Exception as e:
        print("❌ Error al extraer datos desde Supabase:", e)
        return []

    finally:
        cursor.close()

# ====================================
# 🔄 ETAPA: Transformación de usuarios
# ====================================

def transformar_usuarios(usuarios_raw):
    usuarios_limpios = []
    correos_vistos = set()

    for u in usuarios_raw:
        # Validar que tenga correo y sea válido
        correo = u.get('correo', '').strip().lower()
        if not correo or '@' not in correo or correo in correos_vistos:
            continue  # correo inválido o duplicado

        # Limpiar y normalizar campos
        nombre = u.get('nombre', '').strip().title()
        apellido = u.get('apellido', '').strip().title()
        contrasena = u.get('contraseña', '').strip() or "changeme"
        rol = u.get('rol', '').strip().lower()

        # Validar rol
        if rol not in ['estudiante', 'profesor', 'administrador']:
            rol = 'estudiante'  # valor por defecto

        usuario_transformado = {
            "id_usuario": u.get("id_usuario"),
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "contraseña": contrasena,
            "rol": rol
        }

        usuarios_limpios.append(usuario_transformado)
        correos_vistos.add(correo)

    print(f"🧽 {len(usuarios_limpios)} usuarios transformados correctamente")
    return usuarios_limpios


# ====================================
# 📝 ETAPA: Carga a MySQL (SematecPlataform)
# ====================================

def insertar_usuarios_en_mysql(conn, usuarios):
    if not usuarios:
        print("⚠️ No hay usuarios para insertar.")
        return

    try:
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO usuario (id_usuario, nombre, apellido, correo, contraseña, rol)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            nombre = VALUES(nombre),
            apellido = VALUES(apellido),
            correo = VALUES(correo),
            contraseña = VALUES(contraseña),
            rol = VALUES(rol);
        """

        data = [
            (
                u['id_usuario'],
                u['nombre'],
                u['apellido'],
                u['correo'],
                u['contraseña'],
                u['rol']
            )
            for u in usuarios
        ]

        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"✅ {cursor.rowcount} usuarios insertados o actualizados en MySQL")

    except Exception as e:
        print("❌ Error al insertar en MySQL:", e)

    finally:
        cursor.close()
