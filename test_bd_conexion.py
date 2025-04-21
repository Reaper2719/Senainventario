import psycopg2

try:
    # Conectar a la base de datos
    conn = psycopg2.connect(
        dbname='gestiondb',          # Nombre de tu base de datos
        user='postgres',           # Nombre de usuario
        password='Sena2024*',    # Contraseña del usuario postgres
        host='localhost',          # Cambia si es un host diferente
        port='5432'                # Cambia si usas otro puerto
    )
    print("Conexión exitosa a la base de datos.")
    conn.close()
except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
