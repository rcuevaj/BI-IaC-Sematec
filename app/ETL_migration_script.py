import psycopg2
import pymysql
import yaml
from encrypt_yml import decrypt
from modules.user_table_migration import (
    extraer_usuarios_desde_supabase,
    transformar_usuarios,
    insertar_usuarios_en_mysql
)
from modules.perfilprofesor_table_migration import (
    extraer_perfiles_profesor,
    insertar_perfiles_profesor_en_mysql
)
from modules.perfilestudiante_table_migration import (
    extraer_perfiles_estudiante,
    insertar_perfiles_estudiante_en_mysql
)
from modules.curso_table_migration import (
    extraer_cursos_desde_supabase,
    insertar_cursos_en_mysql
)
from modules.inscripcion_table_migration import (
    extraer_inscripciones_desde_supabase,
    transformar_inscripciones,
    insertar_inscripciones_en_mysql,
)
from modules.avancecurso_table_migration import (
    extraer_avances_curso_desde_supabase,
    insertar_avances_curso_en_mysql
)
from modules.evaluacion_table_migration import (
    extraer_evaluaciones_desde_supabase,
    insertar_evaluaciones_en_mysql
)
from modules.resultadoevaluacion_table_migration import (
    extraer_resultados_evaluacion_desde_supabase,
    insertar_resultados_evaluacion_en_mysql
)
from modules.forocurso_table_migration import (
    extraer_foro_curso_desde_supabase,
    insertar_foro_curso_en_mysql
)
from modules.comentarioforo_table_migration import (
    extraer_comentarios_foro_desde_supabase,
    insertar_comentarios_foro_en_mysql
)

# Leer y desencriptar configuración
with open("credential.yml", "r") as f:
    config = yaml.safe_load(f)

# ================================
# 📦 Conexión a Supabase (PostgreSQL)
# ================================
SUPABASE_USER = decrypt(config['app']['DBSupabase']['user'])
SUPABASE_PASSWORD = decrypt(config['app']['DBSupabase']['password'])
SUPABASE_HOST = decrypt(config['app']['DBSupabase']['host'])
SUPABASE_PORT = decrypt(config['app']['DBSupabase']['port'])
SUPABASE_DBNAME = decrypt(config['app']['DBSupabase']['name'])

try:
    supabase_conn = psycopg2.connect(
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD,
        host=SUPABASE_HOST,
        port=SUPABASE_PORT,
        dbname=SUPABASE_DBNAME
    )
    print("✅ Conectado a Supabase PostgreSQL")
except Exception as e:
    print("❌ Error al conectar a Supabase:", e)
    supabase_conn = None

# ================================
# ☁️ Conexión a AWS RDS (MySQL)
# ================================
RDS_USER = decrypt(config['app']['DBSematecPlataform']['user'])
RDS_PASSWORD = decrypt(config['app']['DBSematecPlataform']['password'])
RDS_HOST = decrypt(config['app']['DBSematecPlataform']['host'])
RDS_PORT = int(decrypt(config['app']['DBSematecPlataform']['port']))
RDS_DBNAME = decrypt(config['app']['DBSematecPlataform']['database'])

try:
    rds_conn = pymysql.connect(
        host=RDS_HOST,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DBNAME,
        port=RDS_PORT
    )
    print("✅ Conectado a AWS RDS MySQL")
except pymysql.MySQLError as e:
    print("❌ Error al conectar a AWS RDS:", e)
    rds_conn = None

# ✅ Si ambas conexiones son exitosas, continúas con el ETL
if supabase_conn and rds_conn:
    print("🔄 Conexiones listas para el proceso ETL")
else:
    print("🚫 Conexiones incompletas. Revisa configuración.")

# ====================================
# 🔚 Cierre de conexiones
# ====================================

def cerrar_conexiones(pg_conn, mysql_conn):
    try:
        if pg_conn and not pg_conn.closed:
            pg_conn.close()
            print("🔒 Conexión a Supabase cerrada.")
    except Exception as e:
        print("⚠️ Error al cerrar conexión PostgreSQL:", e)

    try:
        if mysql_conn and mysql_conn.open:
            mysql_conn.close()
            print("🔒 Conexión a AWS RDS MySQL cerrada.")
    except Exception as e:
        print("⚠️ Error al cerrar conexión MySQL:", e)

# ====================================
# ▶️ EJECUCIÓN DEL ETL
# ====================================
if __name__ == "__main__" and supabase_conn and rds_conn:
    print("🚀 Iniciando proceso ETL completo...")

    # 1. Usuario
    usuarios_raw = extraer_usuarios_desde_supabase(supabase_conn)
    usuarios_limpios = transformar_usuarios(usuarios_raw)
    insertar_usuarios_en_mysql(rds_conn, usuarios_limpios)

    # 2. Perfiles
    insertar_perfiles_profesor_en_mysql(rds_conn, extraer_perfiles_profesor(supabase_conn))
    insertar_perfiles_estudiante_en_mysql(rds_conn, extraer_perfiles_estudiante(supabase_conn))

    # 3. Curso
    insertar_cursos_en_mysql(rds_conn, extraer_cursos_desde_supabase(supabase_conn))

    # 4. Evaluación
    insertar_evaluaciones_en_mysql(rds_conn, extraer_evaluaciones_desde_supabase(supabase_conn))

    # 5. Foro
    insertar_foro_curso_en_mysql(rds_conn, extraer_foro_curso_desde_supabase(supabase_conn))

    # 6. Inscripción
    inscripciones_raw = extraer_inscripciones_desde_supabase(supabase_conn)
    inscripciones_limpias = transformar_inscripciones(inscripciones_raw)
    insertar_inscripciones_en_mysql(rds_conn, inscripciones_limpias)

    # 7. Avance de curso
    insertar_avances_curso_en_mysql(rds_conn, extraer_avances_curso_desde_supabase(supabase_conn))

    # 8. Resultados de evaluación
    insertar_resultados_evaluacion_en_mysql(
        rds_conn, extraer_resultados_evaluacion_desde_supabase(supabase_conn)
    )

    # 9. Comentarios de foro
    insertar_comentarios_foro_en_mysql(
        rds_conn, extraer_comentarios_foro_desde_supabase(supabase_conn)
    )

    print("✅ ETL ejecutado con éxito.")
    cerrar_conexiones(supabase_conn, rds_conn)

else:
    print("🚫 No se puede ejecutar ETL: conexión fallida.")