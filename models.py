from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum, Interval, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base
import enum

# Enum para tipo_de_usuario
class TipoUsuarioEnum(str, enum.Enum):
    directivo = "directivo"
    administrador = "administrador"
    analista = "analista"

# Modelo para la tabla usuarios
class Usuario(Base):
    __tablename__ = 'usuarios'

    # Columnas de la tabla
    userid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    correo_electronico = Column(String(255), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    tipo_de_usuario = Column(Enum(TipoUsuarioEnum), nullable=False)

    # Relaciones
    centros = relationship("Centro", back_populates="usuario")
    dispositivos = relationship("Dispositivo", back_populates="usuario")  # Relación bidireccional con dispositivos

    # Restricciones únicas
    __table_args__ = (
        UniqueConstraint('correo_electronico', name='uq_correo_electronico'),
    )

    def __repr__(self):
        """
        Representación en texto para facilitar la depuración.
        """
        return (f"Usuario(userid={self.userid}, nombre='{self.nombre}', "
                f"apellido='{self.apellido}', correo_electronico='{self.correo_electronico}', "
                f"tipo_de_usuario='{self.tipo_de_usuario}')")

# Modelo para la tabla regionales
class Regional(Base):
    __tablename__ = 'regionales'
    regionalid = Column(String, primary_key=True, index=True)  # ID como String
    nombre_de_la_region = Column(String(255), nullable=False)

# Modelo para la tabla centros
class Centro(Base):
    __tablename__ = 'centros'
    centroid = Column(Integer, primary_key=True, index=True)
    nombre_del_centro = Column(String(255), nullable=False)
    ciudad = Column(String(255), nullable=False)
    regionalid = Column(String, ForeignKey('regionales.regionalid'), nullable=False)
    
    usuario_id = Column(Integer, ForeignKey('usuarios.userid'), nullable=False)

    usuario = relationship("Usuario", back_populates="centros")
    
    # Unicidad para combinación nombre y regional
    __table_args__ = (UniqueConstraint('nombre_del_centro', 'regionalid', name='uq_nombre_regional'),)

# Modelo para la tabla sedes
class Sede(Base):
    __tablename__ = 'sedes'
    sedeid = Column(Integer, primary_key=True, index=True)
    nombre_de_la_sede = Column(String(255), nullable=False)
    direccion = Column(String(255), nullable=True)  # Campo opcional

# Tabla intermedia sede_centro
class SedeCentro(Base):
    __tablename__ = 'sede_centro'
    sedeid = Column(Integer, ForeignKey('sedes.sedeid'), primary_key=True)
    centroid = Column(Integer, ForeignKey('centros.centroid'), primary_key=True)

# Modelo para la tabla ambientes
class Ambiente(Base):
    __tablename__ = 'ambientes'
    ambienteid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=True)  # Campo opcional
    tipo_de_circuito = Column(String(255), nullable=True)  # Campo opcional
    sedeid = Column(Integer, ForeignKey('sedes.sedeid'), nullable=False)
    sede = relationship("Sede")

# Modelo para la tabla dispositivos
class Dispositivo(Base):
    __tablename__ = 'dispositivos'
    deviceid = Column(Integer, primary_key=True, index=True)
    nombre_del_dispositivo = Column(String(255), nullable=True)
    descripcion = Column(String, nullable=True)
    consumo_energetico = Column(Float, nullable=True)
    fecha_de_instalacion = Column(Date, nullable=True)
    ambienteid = Column(Integer, ForeignKey('ambientes.ambienteid'), nullable=False)
    ambiente = relationship("Ambiente")
    usuario_id = Column(Integer, ForeignKey('usuarios.userid'), nullable=True)  # Referencia opcional a usuario
    usuario = relationship("Usuario", back_populates="dispositivos")  # Relación bidireccional con usuario

# Modelo para la tabla ocupacion
class Ocupacion(Base):
    __tablename__ = 'ocupacion'
    ocupacionid = Column(Integer, primary_key=True, index=True)
    ambienteid = Column(Integer, ForeignKey('ambientes.ambienteid'), nullable=False)
    cantidad_de_personas = Column(Integer, nullable=True)  # Campo opcional
    tiempo_de_ocupacion = Column(Interval, nullable=True)  # Campo opcional
    fecha = Column(Date, nullable=True)
    ambiente = relationship("Ambiente")

# Modelo para la tabla costos_energia
class CostoEnergia(Base):
    __tablename__ = 'costos_energia'
    costoid = Column(Integer, primary_key=True, index=True)
    sedeid = Column(Integer, ForeignKey('sedes.sedeid'), nullable=False)
    ano = Column(Integer, nullable=True)  # Campo opcional
    mes = Column(Integer, nullable=True)  # Campo opcional
    fecha_inicio_factura = Column(Date, nullable=True)
    fecha_fin_factura = Column(Date, nullable=True)
    consumo_pkwh = Column(Float, nullable=True)
    consumo_qvarh = Column(Float, nullable=True)
    valor_factura = Column(Float, nullable=True)
    contrato = Column(String(255), nullable=True)
    cantidad_aprendices = Column(Integer, nullable=True)
    cantidad_administrativos = Column(Integer, nullable=True)
    sede = relationship("Sede")

# Modelo para la tabla subestaciones
class Subestacion(Base):
    __tablename__ = 'subestaciones'
    subestacionid = Column(Integer, primary_key=True, index=True)
    nombre_sub = Column(String(255), nullable=True)
    sedeid = Column(Integer, ForeignKey('sedes.sedeid'), nullable=False)
    nivel_tension_kva = Column(Float, nullable=True)
    sede = relationship("Sede")
