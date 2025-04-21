import pandas as pd
import psycopg2
import time

# Esperar unos segundos para asegurar que la base de datos esté lista (opcional)
time.sleep(10)

# Leer el archivo Excel (ajusta la ruta si es necesario)
excel_file = 'Sedes_Centros.xlsx'
df = pd.read_excel(excel_file)

# Imprimir los nombres de las columnas para verificar
print("Columnas en el archivo Excel:", df.columns)

# Verificar si hay NaN en las columnas críticas
print("Filas con NaN en la columna 'Sedes':")
print(df[df['Sedes'].isna()])

# Limpiar los datos, reemplazando los NaN con valores vacíos o valores por defecto
df = df.fillna('')

# Asegurarse de que las columnas críticas sean de tipo string
df['Codigo Regional'] = df['Codigo Regional'].astype(str)
df['Regional'] = df['Regional'].astype(str)
df['Cod'] = df['Cod'].astype(str)
df['Descripcion Centro de Costos'] = df['Descripcion Centro de Costos'].astype(str)
df['Sedes'] = df['Sedes'].astype(str)
df['Direccion'] = df['Direccion'].astype(str)
df['Municipio'] = df['Municipio'].astype(str)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='sena2024',  # Reemplaza con tu contraseña de usuario postgres
    host='localhost',     # Cambia 'localhost' si estás usando otro host
    port='5432'           # Cambia el puerto si es diferente
)
cursor = conn.cursor()

# Insertar datos en la tabla regionales
for index, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO regionales (regionalid, nombre_de_la_region) 
        VALUES (%s, %s) 
        ON CONFLICT DO NOTHING
        """,
        (row['Codigo Regional'], row['Regional'])
    )

# Insertar datos en la tabla centros
for index, row in df.iterrows():
    cursor.execute(
        """
        INSERT INTO centros (centroid, nombre_del_centro, ciudad, regionalid) 
        VALUES (%s, %s, %s, %s) 
        ON CONFLICT DO NOTHING
        """,
        (row['Cod'], row['Descripcion Centro de Costos'], row['Municipio'], row['Codigo Regional'])
    )

# Insertar datos en las tablas sedes y sede_centro
for index, row in df.iterrows():
    # Saltar filas donde 'Sedes' está vacío o es 'nan'
    if row['Sedes'] == '' or row['Sedes'].lower() == 'nan':
        continue

    # Verificar si la sede ya existe
    cursor.execute("SELECT sedeid FROM sedes WHERE nombre_de_la_sede = %s", (row['Sedes'],))
    result = cursor.fetchone()

    if result:
        sede_id = result[0]
    else:
        cursor.execute(
            """
            INSERT INTO sedes (nombre_de_la_sede, direccion) 
            VALUES (%s, %s) 
            RETURNING sedeid
            """,
            (row['Sedes'], row['Direccion'])
        )
        sede_id = cursor.fetchone()[0]

    # Insertar en la tabla intermedia sede_centro
    cursor.execute(
        """
        INSERT INTO sede_centro (sedeid, centroid) 
        VALUES (%s, %s) 
        ON CONFLICT DO NOTHING
        """,
        (sede_id, row['Cod'])
    )

# Confirmar los cambios y cerrar la conexión
conn.commit()
cursor.close()
conn.close()

print("Datos insertados correctamente.")
