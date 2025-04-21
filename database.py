from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging

# Configuración de logging para SQLAlchemy
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# URL de conexión a la base de datos
DATABASE_URL = "postgresql://postgres:sena2024@localhost:5432/postgres"

# Crear motor de conexión con manejo de errores
try:
    engine = create_engine(
        DATABASE_URL,
        echo=False,  # Opcional: muestra consultas SQL en el log
        pool_pre_ping=True  # Verifica si las conexiones son válidas antes de usarlas
    )
except Exception as e:
    print("Error al conectar a la base de datos:", e)
    raise

# Crear sesión local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declaración base para modelos de SQLAlchemy
Base = declarative_base()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()