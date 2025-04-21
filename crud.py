from sqlalchemy.orm import Session
from sqlalchemy import func
from models import (Usuario, Regional, Centro, Sede, Ambiente, Dispositivo, CostoEnergia, Ocupacion, Subestacion, SedeCentro)
from fastapi import HTTPException
from typing import Optional, List
from datetime import date
import bcrypt
import models

def create_Usuario(db: Session, Usuario_data: dict):
    Usuario_data["contrasena"] = bcrypt.hashpw(Usuario_data["contrasena"].encoode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    nuevo_usuario = Usuario(**Usuario_data)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

# Función para formatear nombres de ciudad
def format_city_name(city: str) -> str:
    lowercase_words = {"de", "y", "a", "la", "el", "los", "las", "del", "en"}
    words = city.split()
    formatted_words = [word.lower() if word.lower() in lowercase_words else word.capitalize() for word in words]
    return ' '.join(formatted_words)

# **USUARIOS**

# Obtener un usuario por ID
def get_usuario(db: Session, userid: int):
    usuario = db.query(Usuario).filter(Usuario.userid == userid).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

# Crear un nuevo usuario
def create_usuario(db: Session, usuario: Usuario):
    usuario.correo_electronico = usuario.correo_electronico.lower()
    existing_user = db.query(Usuario).filter(Usuario.correo_electronico == usuario.correo_electronico).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado")
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

# Actualizar un usuario existente
def update_usuario(db: Session, userid: int, updated_data: dict):
    usuario = get_usuario(db, userid)
    if usuario:
        if 'correo_electronico' in updated_data:
            updated_data['correo_electronico'] = updated_data['correo_electronico'].lower()
        for key, value in updated_data.items():
            if key != "userid" and value is not None:
                setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
    return usuario

# Eliminar un usuario por ID
def delete_usuario(db: Session, userid: int):
    usuario = get_usuario(db, userid)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(usuario)
    db.commit()
    return usuario

# REGIONALES
def get_regional(db: Session, regionalid: str):
    regional = db.query(Regional).filter(Regional.regionalid == str (regionalid)).first()
    if not regional:
        raise HTTPException(status_code=404, detail="Regional not found")
    return regional

def get_all_regionales(db: Session):
    return db.query(models.Regional).all()

def create_regional(db: Session, regional: models.Regional):
    db.add(regional)
    db.commit()
    db.refresh(regional)
    return regional

def update_regional(db: Session, regionalid: int, updated_data: dict):
    regional = get_regional(db, regionalid)
    if not regional:
        raise HTTPException(status_code=404, detail="Regional not found")
    for key, value in updated_data.items():
        if key != "regionalid" and value is not None:
            setattr(regional, key, value)
    db.commit()
    db.refresh(regional)
    return regional

def delete_regional(db: Session, regionalid: int):
    regional = get_regional(db, regionalid)
    if not regional:
        raise HTTPException(status_code=404, detail="Regional not found")
    db.delete(regional)
    db.commit()
    return regional

# CENTROS
def get_centro(db: Session, centroid: int):
    centro = db.query(models.Centro).filter(models.Centro.centroid == str (centroid)).first()
    if not centro:
        raise HTTPException(status_code=404, detail="Centro not found")
    return centro

def create_centro(db: Session, centro: models.Centro):
    # Verificar si ya existe un centro con el mismo nombre en la misma regional
    existing_centro = db.query(models.Centro).filter(
        models.Centro.nombre_del_centro == centro.nombre_del_centro,
        models.Centro.regionalid == centro.regionalid
    ).first()
    if existing_centro:
        raise HTTPException(status_code=400, detail="El centro con el mismo nombre ya existe en esta regional.")
    db.add(centro)
    db.commit()
    db.refresh(centro)
    return centro

def update_centro(db: Session, centroid: int, updated_data: dict):
    centro = get_centro(db, centroid)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro not found")
    # Verificar si la combinación de nombre y regional cambiaría y causaría un duplicado
    if 'nombre_del_centro' in updated_data and 'regionalid' in updated_data:
        existing_centro = db.query(models.Centro).filter(
            models.Centro.nombre_del_centro == updated_data['nombre_del_centro'],
            models.Centro.regionalid == updated_data['regionalid'],
            models.Centro.centroid != centroid  # Excluir el registro actual
        ).first()
        if existing_centro:
            raise HTTPException(status_code=400, detail="El centro con el mismo nombre ya existe en esta regional.")

    for key, value in updated_data.items():
        if value is not None:
            setattr(centro, key, value)
    db.commit()
    db.refresh(centro)
    return centro

def delete_centro(db: Session, centroid: int):
    centro = get_centro(db, centroid)
    if not centro:
        raise HTTPException(status_code=404, detail="Centro not found")
    db.delete(centro)
    db.commit()
    return centro

# SEDES
def get_sede(db: Session, sedeid: int):
    sede = db.query(models.Sede).filter(models.Sede.sedeid == str (sedeid)).first()
    if not sede:
        raise HTTPException(status_code=404, detail="Sede not found")
    return sede

def create_sede(db: Session, sede: models.Sede):
    db.add(sede)
    db.commit()
    db.refresh(sede)
    return sede

def update_sede(db: Session, sedeid: int, updated_data: dict):
    sede = get_sede(db, sedeid)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede not found")
    for key, value in updated_data.items():
        if key != "sedeid" and value is not None:
            setattr(sede, key, value)
    db.commit()
    db.refresh(sede)
    return sede

def delete_sede(db: Session, sedeid: int):
    sede = get_sede(db, sedeid)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede not found")
    db.delete(sede)
    db.commit()
    return sede

# AMBIENTES
def get_ambiente(db: Session, ambienteid: int):
    ambiente = db.query(models.Ambiente).filter(models.Ambiente.ambienteid == str (ambienteid)).first()
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente not found")
    return ambiente

def create_ambiente(db: Session, ambiente: models.Ambiente):
    db.add(ambiente)
    db.commit()
    db.refresh(ambiente)
    return ambiente

def update_ambiente(db: Session, ambienteid: int, updated_data: dict):
    ambiente = get_ambiente(db, ambienteid)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente not found")
    for key, value in updated_data.items():
        if key != "ambienteid" and value is not None:
            setattr(ambiente, key, value)
    db.commit()
    db.refresh(ambiente)
    return ambiente

def delete_ambiente(db: Session, ambienteid: int):
    ambiente = get_ambiente(db, ambienteid)
    if not ambiente:
        raise HTTPException(status_code=404, detail="Ambiente not found")
    db.delete(ambiente)
    db.commit()
    return ambiente

# DISPOSITIVOS
def get_dispositivo(db: Session, deviceid: int):
    dispositivo = db.query(models.Dispositivo).filter(models.Dispositivo.deviceid == str (deviceid)).first()
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    return dispositivo

def create_dispositivo(db: Session, dispositivo: models.Dispositivo):
    db.add(dispositivo)
    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def update_dispositivo(db: Session, deviceid: int, updated_data: dict):
    dispositivo = get_dispositivo(db, deviceid)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    for key, value in updated_data.items():
        if key != "deviceid" and value is not None:
            setattr(dispositivo, key, value)
    db.commit()
    db.refresh(dispositivo)
    return dispositivo

def delete_dispositivo(db: Session, deviceid: int):
    dispositivo = get_dispositivo(db, deviceid)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo not found")
    db.delete(dispositivo)
    db.commit()
    return dispositivo

# OCUPACION
def get_ocupacion(db: Session, ocupacionid: int):
    ocupacion = db.query(models.Ocupacion).filter(models.Ocupacion.ocupacionid == str (ocupacionid)).first()
    if not ocupacion:
        raise HTTPException(status_code=404, detail="Ocupacion not found")
    return ocupacion

def create_ocupacion(db: Session, ocupacion: models.Ocupacion):
    db.add(ocupacion)
    db.commit()
    db.refresh(ocupacion)
    return ocupacion

def update_ocupacion(db: Session, ocupacionid: int, updated_data: dict):
    ocupacion = get_ocupacion(db, ocupacionid)
    if not ocupacion:
        raise HTTPException(status_code=404, detail="Ocupacion not found")
    for key, value in updated_data.items():
        if key != "ocupacionid" and value is not None:
            setattr(ocupacion, key, value)
    db.commit()
    db.refresh(ocupacion)
    return ocupacion

def delete_ocupacion(db: Session, ocupacionid: int):
    ocupacion = get_ocupacion(db, ocupacionid)
    if not ocupacion:
        raise HTTPException(status_code=404, detail="Ocupacion not found")
    db.delete(ocupacion)
    db.commit()
    return ocupacion

# COSTOS_ENERGIA
def get_costo_energia(db: Session, costoid: int):
    costo_energia = db.query(models.CostoEnergia).filter(models.CostoEnergia.costoid == str (costoid)).first()
    if not costo_energia:
        raise HTTPException(status_code=404, detail="CostoEnergia not found")
    return costo_energia

def create_costo_energia(db: Session, costo_energia: models.CostoEnergia):
    db.add(costo_energia)
    db.commit()
    db.refresh(costo_energia)
    return costo_energia

def update_costo_energia(db: Session, costoid: int, updated_data: dict):
    costo = get_costo_energia(db, costoid)
    if not costo:
        raise HTTPException(status_code=404, detail="CostoEnergia not found")
    for key, value in updated_data.items():
        if key != "costoid" and value is not None:
            setattr(costo, key, value)
    db.commit()
    db.refresh(costo)
    return costo

def delete_costo_energia(db: Session, costoid: int):
    costo = get_costo_energia(db, costoid)
    if not costo:
        raise HTTPException(status_code=404, detail="CostoEnergia not found")
    db.delete(costo)
    db.commit()
    return costo

# SUBESTACIONES
def get_subestacion(db: Session, subestacionid: int):
    subestacion = db.query(models.Subestacion).filter(models.Subestacion.subestacionid == str (subestacionid)).first()
    if not subestacion:
        raise HTTPException(status_code=404, detail="Subestacion not found")
    return subestacion

def create_subestacion(db: Session, subestacion: models.Subestacion):
    db.add(subestacion)
    db.commit()
    db.refresh(subestacion)
    return subestacion

def update_subestacion(db: Session, subestacionid: int, updated_data: dict):
    subestacion = get_subestacion(db, subestacionid)
    if not subestacion:
        raise HTTPException(status_code=404, detail="Subestacion not found")
    for key, value in updated_data.items():
        if key != "subestacionid" and value is not None:
            setattr(subestacion, key, value)
    db.commit()
    db.refresh(subestacion)
    return subestacion

def delete_subestacion(db: Session, subestacionid: int):
    subestacion = get_subestacion(db, subestacionid)
    if not subestacion:
        raise HTTPException(status_code=404, detail="Subestacion not found")
    db.delete(subestacion)
    db.commit()
    return subestacion

# USUARIOS
def get_usuarios_by_tipo(db: Session, tipo_de_usuario: str):
    usuarios = db.query(Usuario).filter(Usuario.tipo_de_usuario == str (tipo_de_usuario)).all()
    return usuarios

def get_usuario_by_correo(db: Session, correo_electronico: str):
    usuario = db.query(Usuario).filter(Usuario.correo_electronico == correo_electronico).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario not found")
    return usuario

# CENTROS
def get_centros_by_region(db: Session, regionalid: int):
    centros = db.query(Centro).filter(Centro.regionalid == str (regionalid)).all()
    return centros

# SEDES
def get_sedes_by_centro(db: Session, centro_id: int):
    sedes = db.query(SedeCentro).filter(SedeCentro.centroid == str (centro_id)).all()
    return [sede.sedeid for sede in sedes]

# AMBIENTES
def get_ambientes_by_sede(db: Session, sedeid: int):
    ambientes = db.query(Ambiente).filter(Ambiente.sedeid == str (sedeid)).all()
    return ambientes

def get_ambientes_por_tipo_de_circuito(db: Session, tipo_de_circuito: str):
    ambientes = db.query(Ambiente).filter(Ambiente.tipo_de_circuito == tipo_de_circuito).all()
    return ambientes

# DISPOSITIVOS
def get_dispositivos_by_ambiente(db: Session, ambienteid: int):
    dispositivos = db.query(Dispositivo).filter(Dispositivo.ambienteid == str (ambienteid)).all()
    return dispositivos

def get_dispositivos_por_fecha_instalacion(db: Session, fecha_inicio, fecha_fin):
    dispositivos = db.query(Dispositivo).filter(Dispositivo.fecha_de_instalacion.between(fecha_inicio, fecha_fin)).all()
    return dispositivos

def obtener_dispositivos_alto_consumo(db: Session, ambienteid: int, consumo_minimo: float):
    dispositivos = db.query(Dispositivo).filter(Dispositivo.ambienteid == ambienteid, Dispositivo.consumo_energetico > consumo_minimo).all()
    return dispositivos

# COSTOS ENERGÍA
def get_costos_energia_por_ano_mes(db: Session, sedeid: int, año: int, mes: int):
    costos = db.query(CostoEnergia).filter(CostoEnergia.sedeid == sedeid, CostoEnergia.año == año, CostoEnergia.mes == str (mes)).all()
    return costos

def get_consumo_energetico_por_fecha(db: Session, sedeid: int, fecha_inicio, fecha_fin):
    consumo = db.query(CostoEnergia).filter(CostoEnergia.sedeid == sedeid, CostoEnergia.fecha_inicio_factura.between(fecha_inicio, fecha_fin)).all()
    return consumo

# OCUPACIÓN
def obtener_ocupacion_promedio(db: Session, ambienteid: int, fecha_inicio, fecha_fin):
    ocupacion_promedio = db.query(func.avg(Ocupacion.cantidad_de_personas)).filter(Ocupacion.ambienteid == ambienteid, Ocupacion.fecha.between == str (fecha_inicio, fecha_fin)).scalar()
    return ocupacion_promedio

def get_ocupacion_por_ambiente_y_fecha(db: Session, ambienteid: int, fecha):
    ocupacion = db.query(Ocupacion).filter(Ocupacion.ambienteid == ambienteid, Ocupacion.fecha == str (fecha)).all()
    return ocupacion

# SUBESTACIONES
def get_subestaciones_por_sede(db: Session, sedeid: int):
    subestaciones = db.query(Subestacion).filter(Subestacion.sedeid == str (sedeid)).all()
    return subestaciones

def obtener_subestaciones_por_nivel_tension(db: Session, nivel_tension_kva: float):
    subestaciones = db.query(Subestacion).filter(Subestacion.nivel_tension_kva == nivel_tension_kva).all()
    return subestaciones