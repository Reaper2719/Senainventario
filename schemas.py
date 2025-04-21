from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional
from datetime import date, timedelta
from enum import Enum
from pydantic import BaseModel

class RecuperarcontrasenaRequest(BaseModel):
    correo_electronico: str

# Enum for tipo_de_usuario
class TipoUsuarioEnum(str, Enum):
    directivo = "directivo"
    administrador = "administrador"
    analista = "analista"

# Pydantic schema for Usuario with non-nullable fields
class UsuarioBase(BaseModel):
    nombre: constr(min_length=1, max_length=255) # type: ignore
    apellido: constr(min_length=1, max_length=255) # type: ignore
    correo_electronico: EmailStr
    tipo_de_usuario: TipoUsuarioEnum

class UsuarioCreate(UsuarioBase):
    contrasena: constr(min_length=8, max_length=128) # type: ignore

    @validator('correo_electronico')
    def validate_email(cls, correo_electronico):
        return correo_electronico.lower()

    @validator('nombre', 'apellido')
    def validate_name(cls, value):
        if not value.isalpha():
            raise ValueError('El nombre y el apellido deben contener solo letras.')
        return value.capitalize()

    @validator('contrasena')
    def validate_password(cls, value):
        if not any(char.isdigit() for char in value):
            raise ValueError('La contraseña debe contener al menos un número.')
        if not any(char.isupper() for char in value):
            raise ValueError('La contraseña debe contener al menos una letra mayúscula.')
        if not any(char.islower() for char in value):
            raise ValueError('La contraseña debe contener al menos una letra minúscula.')
        return value

class Usuario(UsuarioBase):
    userid: int

    class Config:
        from_attributes = True

class UsuarioOut(UsuarioBase):
    userid: int

    class Config:
        from_attributes = True

# Pydantic schema for Regional with non-nullable fields
class RegionalBase(BaseModel):
    nombre_de_la_region: constr(min_length=1, max_length=255) # type: ignore

class RegionalCreate(RegionalBase):
    nombre_de_la_region: constr(min_length=1, max_length=255) # type: ignore

class Regional(RegionalBase):
    regionalid: int

    class Config:
        from_attributes = True

# Pydantic schema for Centro with non-nullable fields
class CentroBase(BaseModel):
    nombre_del_centro: constr(min_length=1, max_length=255) # type: ignore
    ciudad: constr(min_length=1, max_length=255) # type: ignore
    regionalid: int

class CentroCreate(CentroBase):
    nombre_del_centro: constr(min_length=1, max_length=255) # type: ignore
    ciudad: constr(min_length=1, max_length=255) # type: ignore
    regionalid: int

class Centro(CentroBase):
    centroid: int

    class Config:
        from_attributes = True

# Pydantic schema for Sede with non-nullable fields
class SedeBase(BaseModel):
    nombre_de_la_sede: constr(min_length=1, max_length=255) # type: ignore
    direccion: Optional[str] = None

class SedeCreate(SedeBase):
    nombre_de_la_sede: constr(min_length=1, max_length=255) # type: ignore
    direccion: Optional[str] = None

class Sede(SedeBase):
    sedeid: int

    class Config:
        from_attributes = True

# Pydantic schema for SedeCentro
class SedeCentroBase(BaseModel):
    sedeid: int
    centroid: int

class SedeCentro(SedeCentroBase):
    sedeid: int
    centroid: int

    class Config:
        from_attributes = True

# Pydantic schema for Ambiente with optional fields
class AmbienteBase(BaseModel):
    nombre: Optional[str] = None
    tipo_de_circuito: Optional[str] = None
    sedeid: int

class AmbienteCreate(AmbienteBase):
    nombre: Optional[str] = None
    tipo_de_circuito: Optional[str] = None
    sedeid: int

class Ambiente(AmbienteBase):
    ambienteid: int

    class Config:
        from_attributes = True

# Pydantic schema for Dispositivo with optional fields
class DispositivoBase(BaseModel):
    nombre_del_dispositivo: Optional[str] = None
    descripcion: Optional[str] = None
    consumo_energetico: Optional[float] = None
    fecha_de_instalacion: Optional[date] = None
    ambienteid: int
    tipo_de_lugar: Optional[str] = None
    referencias_a_mediciones: Optional[str] = None

class DispositivoCreate(DispositivoBase):
    nombre_del_dispositivo: Optional[str] = None
    descripcion: Optional[str] = None
    consumo_energetico: Optional[float] = None
    fecha_de_instalacion: Optional[date] = None
    ambienteid: int
    tipo_de_lugar: Optional[str] = None
    referencias_a_mediciones: Optional[str] = None

class Dispositivo(DispositivoBase):
    deviceid: int

    class Config:
        from_attributes = True

# Pydantic schema for Ocupacion with optional fields
class OcupacionBase(BaseModel):
    ambienteid: int
    cantidad_de_personas: Optional[int] = None
    tiempo_de_ocupacion: Optional[timedelta] = None
    fecha: Optional[date] = None

class OcupacionCreate(OcupacionBase):
    ambienteid: int
    cantidad_de_personas: Optional[int] = None
    tiempo_de_ocupacion: Optional[timedelta] = None
    fecha: Optional[date] = None

class Ocupacion(OcupacionBase):
    ocupacionid: int

    class Config:
        from_attributes = True

class OcupacionOut(BaseModel):
    ocupacionid: int
    ambienteid: int
    cantidad_de_personas: Optional[int] = None
    tiempo_de_ocupacion: Optional[timedelta] = None
    fecha: Optional[date] = None

    class Config:
        from_attributes = True

class ResumenConsumo(BaseModel):
    total_consumo_kw: float
    total_consumo_qvarh: float
    total_valor_factura: float

# Pydantic schema for CostoEnergia with optional fields
class CostoEnergiaBase(BaseModel):
    sedeid: int
    ano: Optional[int] = None
    mes: Optional[int] = None
    fecha_inicio_factura: Optional[date] = None
    fecha_fin_factura: Optional[date] = None
    consumo_pkwh: Optional[float] = None
    consumo_qvarh: Optional[float] = None
    valor_factura: Optional[float] = None
    contrato: Optional[str] = None
    cantidad_aprendices: Optional[int] = None
    cantidad_administrativos: Optional[int] = None

class CostoEnergiaCreate(CostoEnergiaBase):
    sedeid: int
    año: Optional[int] = None
    mes: Optional[int] = None
    fecha_inicio_factura: Optional[date] = None
    fecha_fin_factura: Optional[date] = None
    consumo_pkwh: Optional[float] = None
    consumo_qvarh: Optional[float] = None
    valor_factura: Optional[float] = None
    contrato: Optional[str] = None
    cantidad_aprendices: Optional[int] = None
    cantidad_administrativos: Optional[int] = None

class CostoEnergia(CostoEnergiaBase):
    costoid: int

    class Config:
        from_attributes = True

# Pydantic schema for Subestacion with optional fields
class SubestacionBase(BaseModel):
    nombre_sub: Optional[str] = None
    sedeid: int
    nivel_tension_kva: Optional[float] = None

class SubestacionCreate(SubestacionBase):
    nombre_sub: Optional[str] = None
    sedeid: int
    nivel_tension_kva: Optional[float] = None

class Subestacion(SubestacionBase):
    subestacionid: int

    class Config:
        from_attributes = True