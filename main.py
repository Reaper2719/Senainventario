from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
import logging
from datetime import date
from typing import Optional, List
import crud
import models, schemas
from database import engine, get_db

# Configuración de logging para depuración
logging.basicConfig(level=logging.DEBUG)

# Instancia de FastAPI
app = FastAPI()

# Montar directorio estático para servir archivos como HTML, CSS, JS, etc.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configuración de CORS para permitir solicitudes desde otros orígenes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Dominios específicos
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Definición de modelos para solicitud de login y recuperación de contraseña
class LoginRequest(BaseModel):
    correo_electronico: EmailStr
    contrasena: str

# Login
@app.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.correo_electronico == request.correo_electronico).first()
    if not usuario or usuario.contrasena != request.contrasena:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    return {"message": "Login exitoso", "usuario_id": usuario.nombre}

# Endpoint para obtener usuarios por tipo de usuario
@app.get("/usuarios/tipo/{tipo_usuario}", response_model=List[schemas.Usuario])
def read_usuarios_by_tipo(tipo_usuario: str, db: Session = Depends(get_db)):
    return crud.get_usuarios_by_tipo(db=db, tipo_usuario=tipo_usuario)

# Endpoint para obtener un usuario por correo electrónico
@app.get("/usuarios/correo/{correo_electronico}", response_model=schemas.Usuario)
def read_usuario_by_correo(correo_electronico: str, db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_correo(db=db, correo_electronico=correo_electronico)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

# Ruta raíz
@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API"}

# Crear todas las tablas si no existen
models.Base.metadata.create_all(bind=engine)

# **USUARIOS**

# Obtener un usuario por ID
@app.get("/usuarios/{userid}", response_model=schemas.Usuario)
def read_usuario(userid: int, db: Session = Depends(get_db)):
   
    usuario = crud.get_usuario(db, userid=userid)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

# Crear un nuevo usuario
@app.post("/usuarios/", response_model=schemas.Usuario)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
   
    try:
        # Crear el usuario en la base de datos
        usuario_db = models.Usuario(**usuario.dict())
        return crud.create_usuario(db=db, usuario=usuario_db)
    except Exception as e:
        # Manejar errores y devolver un mensaje claro
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

# Actualizar un usuario existente
@app.put("/usuarios/{userid}", response_model=schemas.Usuario)
def update_usuario(userid: int, usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    return crud.update_usuario(db=db, userid=userid, updated_data=usuario.dict(exclude_unset=True))

# Eliminar un usuario por ID
@app.delete("/usuarios/{userid}", response_model=dict)
def delete_usuario(userid: int, db: Session = Depends(get_db)):
    usuario = crud.delete_usuario(db, userid=userid)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return {"detail": "Usuario eliminado con éxito"}

# **Ejecución del Servidor**
if __name__ == "__main__":
    import uvicorn
    # Agregado reload=True para facilitar el desarrollo
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# REGIONALES
@app.get("/regionales/", response_model=List[schemas.Regional])
def read_regionales(db: Session = Depends(get_db)):
    return crud.get_all_regionales(db)

@app.get("/regionales/{regionalid}", response_model=schemas.Regional)
def read_regional(regionalid: str, db: Session = Depends(get_db)):
    regional = crud.get_regional(db, regionalid=regionalid)
    if not regional:
        raise HTTPException(status_code=404, detail="Regional not found")
    return regional

@app.post("/regionales/", response_model=schemas.Regional)
def create_regional(regional: schemas.RegionalCreate, db: Session = Depends(get_db)):
    regional_db = models.Regional(**regional.dict())
    return crud.create_regional(db=db, regional=regional_db)

@app.put("/regionales/{regionalid}", response_model=schemas.Regional)
def update_regional(regionalid: int, regional: schemas.RegionalCreate, db: Session = Depends(get_db)):
    return crud.update_regional(db=db, regionalid=regionalid, updated_data=regional.dict(exclude_unset=True))

@app.delete("/regionales/{regionalid}", response_model=dict)
def delete_regional(regionalid: int, db: Session = Depends(get_db)):
    regional = crud.delete_regional(db, regionalid=regionalid)
    if regional is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Regional not found")
    return {"detail": "Regional deleted"}

# CENTROS
@app.get("/centros/{centroid}", response_model=schemas.Centro)
def read_centro(centroid: int, db: Session = Depends(get_db)):
    centro = crud.get_centro(db, centroid=centroid)
    if centro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro not found")
    return centro

@app.post("/centros/", response_model=schemas.Centro)
def create_centro(centro: schemas.CentroCreate, db: Session = Depends(get_db)):
    centro_db = models.Centro(**centro.dict())
    return crud.create_centro(db=db, centro=centro_db)

@app.put("/centros/{centroid}", response_model=schemas.Centro)
def update_centro(centroid: int, centro: schemas.CentroCreate, db: Session = Depends(get_db)):
    return crud.update_centro(db=db, centroid=centroid, updated_data=centro.dict(exclude_unset=True))

@app.delete("/centros/{centroid}", response_model=dict)
def delete_centro(centroid: int, db: Session = Depends(get_db)):
    centro = crud.delete_centro(db, centroid=centroid)
    if centro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Centro not found")
    return {"detail": "Centro deleted"}

# SEDES
@app.get("/sedes/{sedeid}", response_model=schemas.Sede)
def read_sede(sedeid: int, db: Session = Depends(get_db)):
    sede = crud.get_sede(db, sedeid=sedeid)
    if sede is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sede not found")
    return sede

@app.post("/sedes/", response_model=schemas.Sede)
def create_sede(sede: schemas.SedeCreate, db: Session = Depends(get_db)):
    sede_db = models.Sede(**sede.dict())
    return crud.create_sede(db=db, sede=sede_db)

@app.put("/sedes/{sedeid}", response_model=schemas.Sede)
def update_sede(sedeid: int, sede: schemas.SedeCreate, db: Session = Depends(get_db)):
    return crud.update_sede(db=db, sedeid=sedeid, updated_data=sede.dict(exclude_unset=True))

@app.delete("/sedes/{sedeid}", response_model=dict)
def delete_sede(sedeid: int, db: Session = Depends(get_db)):
    sede = crud.delete_sede(db, sedeid=sedeid)
    if sede is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sede not found")
    return {"detail": "Sede deleted"}

# AMBIENTES
@app.get("/ambientes/{ambienteid}", response_model=schemas.Ambiente)
def read_ambiente(ambienteid: int, db: Session = Depends(get_db)):
    ambiente = crud.get_ambiente(db, ambienteid=ambienteid)
    if ambiente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ambiente not found")
    return ambiente

@app.post("/ambientes/", response_model=schemas.Ambiente)
def create_ambiente(ambiente: schemas.AmbienteCreate, db: Session = Depends(get_db)):
    ambiente_db = models.Ambiente(**ambiente.dict())
    return crud.create_ambiente(db=db, ambiente=ambiente_db)

@app.put("/ambientes/{ambienteid}", response_model=schemas.Ambiente)
def update_ambiente(ambienteid: int, ambiente: schemas.AmbienteCreate, db: Session = Depends(get_db)):
    return crud.update_ambiente(db=db, ambienteid=ambienteid, updated_data=ambiente.dict(exclude_unset=True))

@app.delete("/ambientes/{ambienteid}", response_model=dict)
def delete_ambiente(ambienteid: int, db: Session = Depends(get_db)):
    ambiente = crud.delete_ambiente(db, ambienteid=ambienteid)
    if ambiente is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ambiente not found")
    return {"detail": "Ambiente deleted"}

# DISPOSITIVOS
@app.get("/dispositivos/{deviceid}", response_model=schemas.Dispositivo)
def read_dispositivo(deviceid: int, db: Session = Depends(get_db)):
    dispositivo = crud.get_dispositivo(db, deviceid=deviceid)
    if dispositivo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo not found")
    return dispositivo

@app.post("/dispositivos/", response_model=schemas.Dispositivo)
def create_dispositivo(dispositivo: schemas.DispositivoCreate, db: Session = Depends(get_db)):
    dispositivo_db = models.Dispositivo(**dispositivo.dict())
    return crud.create_dispositivo(db=db, dispositivo=dispositivo_db)

@app.put("/dispositivos/{deviceid}", response_model=schemas.Dispositivo)
def update_dispositivo(deviceid: int, dispositivo: schemas.DispositivoCreate, db: Session = Depends(get_db)):
    return crud.update_dispositivo(db=db, deviceid=deviceid, updated_data=dispositivo.dict(exclude_unset=True))

@app.delete("/dispositivos/{deviceid}", response_model=dict)
def delete_dispositivo(deviceid: int, db: Session = Depends(get_db)):
    dispositivo = crud.delete_dispositivo(db, deviceid=deviceid)
    if dispositivo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dispositivo not found")
    return {"detail": "Dispositivo deleted"}

# OCUPACION
@app.get("/ocupacion/{ocupacionid}", response_model=schemas.Ocupacion)
def read_ocupacion(ocupacionid: int, db: Session = Depends(get_db)):
    ocupacion = crud.get_ocupacion(db, ocupacionid=ocupacionid)
    if ocupacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ocupacion not found")
    return ocupacion

@app.post("/ocupacion/", response_model=schemas.Ocupacion)
def create_ocupacion(ocupacion: schemas.OcupacionCreate, db: Session = Depends(get_db)):
    ocupacion_db = models.Ocupacion(**ocupacion.dict())
    return crud.create_ocupacion(db=db, ocupacion=ocupacion_db)

@app.put("/ocupacion/{ocupacionid}", response_model=schemas.Ocupacion)
def update_ocupacion(ocupacionid: int, ocupacion: schemas.OcupacionCreate, db: Session = Depends(get_db)):
    return crud.update_ocupacion(db=db, ocupacionid=ocupacionid, updated_data=ocupacion.dict(exclude_unset=True))

@app.delete("/ocupacion/{ocupacionid}", response_model=dict)
def delete_ocupacion(ocupacionid: int, db: Session = Depends(get_db)):
    ocupacion = crud.delete_ocupacion(db, ocupacionid=ocupacionid)
    if ocupacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ocupacion not found")
    return {"detail": "Ocupacion deleted"}

# COSTOS_ENERGIA
@app.get("/costos_energia/{costoid}", response_model=schemas.CostoEnergia)
def read_costo_energia(costoid: int, db: Session = Depends(get_db)):
    costo_energia = crud.get_costo_energia(db, costoid=costoid)
    if costo_energia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CostoEnergia not found")
    return costo_energia

@app.post("/costos_energia/", response_model=schemas.CostoEnergia)
def create_costo_energia(costo_energia: schemas.CostoEnergiaCreate, db: Session = Depends(get_db)):
    costo_energia_db = models.CostoEnergia(**costo_energia.dict())
    return crud.create_costo_energia(db=db, costo_energia=costo_energia_db)

@app.put("/costos_energia/{costoid}", response_model=schemas.CostoEnergia)
def update_costo_energia(costoid: int, costo_energia: schemas.CostoEnergiaCreate, db: Session = Depends(get_db)):
    return crud.update_costo_energia(db=db, costoid=costoid, updated_data=costo_energia.dict(exclude_unset=True))

@app.delete("/costos_energia/{costoid}", response_model=dict)
def delete_costo_energia(costoid: int, db: Session = Depends(get_db)):
    costo_energia = crud.delete_costo_energia(db, costoid=costoid)
    if costo_energia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CostoEnergia not found")
    return {"detail": "CostoEnergia deleted"}

# SUBESTACIONES
@app.get("/subestaciones/{subestacionid}", response_model=schemas.Subestacion)
def read_subestacion(subestacionid: int, db: Session = Depends(get_db)):
    subestacion = crud.get_subestacion(db, subestacionid=subestacionid)
    if subestacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subestacion not found")
    return subestacion

@app.post("/subestaciones/", response_model=schemas.Subestacion)
def create_subestacion(subestacion: schemas.SubestacionCreate, db: Session = Depends(get_db)):
    subestacion_db = models.Subestacion(**subestacion.dict())
    return crud.create_subestacion(db=db, subestacion=subestacion_db)

@app.put("/subestaciones/{subestacionid}", response_model=schemas.Subestacion)
def update_subestacion(subestacionid: int, subestacion: schemas.SubestacionCreate, db: Session = Depends(get_db)):
    return crud.update_subestacion(db=db, subestacionid=subestacionid, updated_data=subestacion.dict(exclude_unset=True))

@app.delete("/subestaciones/{subestacionid}", response_model=dict)
def delete_subestacion(subestacionid: int, db: Session = Depends(get_db)):
    subestacion = crud.delete_subestacion(db, subestacionid=subestacionid)
    if subestacion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subestacion not found")
    return {"detail": "Subestacion deleted"}

#****************************************ENDPOINTs CONSULTAS*****************************************************************
# Endpoint para obtener usuarios por tipo de usuario
@app.get("/usuarios/tipo/{tipo_usuario}", response_model=List[schemas.Usuario])
def read_usuarios_by_tipo(tipo_usuario: str, db: Session = Depends(get_db)):
    return crud.get_usuarios_by_tipo(db=db, tipo_usuario=tipo_usuario)

# Endpoint para obtener un usuario por correo electrónico
@app.get("/usuarios/correo/{correo_electronico}", response_model=schemas.Usuario)
def read_usuario_by_correo(correo_electronico: str, db: Session = Depends(get_db)):
    usuario = crud.get_usuario_by_correo(db=db, correo_electronico=correo_electronico)
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

@app.get("/consulta/correo")
def consulta_correo_y_tipo(
    correo_electronico: str,
    tipo_usuario: str,
    db: Session = Depends(get_db)
):
    usuario = db.query(models.Usuario).filter(
        models.Usuario.correo_electronico == correo_electronico,
        models.Usuario.tipo_de_usuario == tipo_usuario
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {
        "nombre": usuario.nombre,
        "correo_electronico": usuario.correo_electronico,
        "tipo_usuario": usuario.tipo_de_usuario
    }

# Endpoint para obtener centros por región
@app.get("/centros/regional/{regionalid}", response_model=List[schemas.Centro])
def read_centros_by_region(regionalid: int, db: Session = Depends(get_db)):
    return crud.get_centros_by_region(db=db, regionalid=regionalid)

# Endpoint para obtener sedes por centro
@app.get("/sedes/centro/{centro_id}", response_model=List[schemas.Sede])
def read_sedes_by_centro(centro_id: int, db: Session = Depends(get_db)):
    sedes = crud.get_sedes_by_centro(db=db, centroid=centroid) # type: ignore
    if not sedes:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron sedes para este centro.")
    return sedes

# Endpoint para obtener ambientes por sede
@app.get("/ambientes/sede/{sedeid}", response_model=List[schemas.Ambiente])
def read_ambientes_by_sede(sedeid: int, db: Session = Depends(get_db)):
    ambientes = crud.get_ambientes_by_sede(db=db, sedeid=sedeid)
    if not ambientes:
        raise HTTPException(status_code=404, detail="No se encontraron ambientes para esta sede.")
    return ambientes

# Endpoint para obtener dispositivos por ambiente
@app.get("/dispositivos/ambiente/{ambienteid}", response_model=List[schemas.Dispositivo])
def read_dispositivos_by_ambiente(ambienteid: int, db: Session = Depends(get_db)):
    dispositivos = crud.get_dispositivos_by_ambiente(db=db, ambienteid=ambienteid)
    if not dispositivos:
        raise HTTPException(status_code=404, detail="No se encontraron dispositivos para este ambiente.")
    return dispositivos

# Endpoint para obtener consumo energético por fecha
@app.get("/consumo/energia/{sedeid}", response_model=List[schemas.CostoEnergia])
def read_consumo_energetico_por_fecha(sedeid: int, fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    consumo = crud.get_consumo_energetico_por_fecha(db=db, sedeid=sedeid, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    if not consumo:
        raise HTTPException(status_code=404, detail="No se encontró consumo energético en el rango de fechas proporcionado.")
    return consumo

# Endpoint para obtener costos de energía por año y mes
@app.get("/costos/energia/{sedeid}/{ano}/{mes}", response_model=List[schemas.CostoEnergia])
def read_costos_energia_por_ano_mes(sedeid: int, ano: int, mes: int, db: Session = Depends(get_db)):
    costos = crud.get_costos_energia_por_ano_mes(db=db, sedeid=sedeid, ano=ano, mes=mes)
    if not costos:
        raise HTTPException(status_code=404, detail="No se encontraron costos de energía para el año y mes proporcionados.")
    return costos

# Endpoint para obtener ocupación por ambiente y fecha
@app.get("/ocupacion/ambiente/{ambienteid}/{fecha}", response_model=List[schemas.Ocupacion])
def read_ocupacion_por_ambiente_y_fecha(ambienteid: int, fecha: date, db: Session = Depends(get_db)):
    ocupacion = crud.get_ocupacion_por_ambiente_y_fecha(db=db, ambienteid=ambienteid, fecha=fecha)
    if not ocupacion:
        raise HTTPException(status_code=404, detail="No se encontró ocupación para el ambiente y fecha proporcionados.")
    return ocupacion

# Endpoint para obtener subestaciones por sede
@app.get("/subestaciones/sede/{sedeid}", response_model=List[schemas.Subestacion])
def read_subestaciones_por_sede(sedeid: int, db: Session = Depends(get_db)):
    subestaciones = crud.get_subestaciones_por_sede(db=db, sedeid=sedeid)
    if not subestaciones:
        raise HTTPException(status_code=404, detail="No se encontraron subestaciones para esta sede.")
    return subestaciones

# Endpoint para obtener centros por ciudad
@app.get("/centros/ciudad/{ciudad}", response_model=List[schemas.Centro])
def read_centros_por_ciudad(ciudad: str, db: Session = Depends(get_db)):
    centros = crud.get_centros_por_ciudad(db=db, ciudad=ciudad)
    if not centros:
        raise HTTPException(status_code=404, detail="No se encontraron centros para la ciudad proporcionada.")
    return centros

# Endpoint para obtener resumen de consumo total por región
@app.get("/resumen/consumo/region/{regionalid}", response_model=schemas.ResumenConsumo)
def read_resumen_consumo_total_por_region(regionalid: int, db: Session = Depends(get_db)):
    resumen = crud.get_resumen_consumo_total_por_region(db=db, regionalid=regionalid)
    if not resumen:
        raise HTTPException(status_code=404, detail="No se encontró resumen de consumo para esta región.")
    return resumen

# Endpoint para obtener ambientes por tipo de circuito
@app.get("/ambientes/tipo/{tipo_circuito}", response_model=List[schemas.Ambiente])
def read_ambientes_por_tipo_de_circuito(tipo_circuito: str, db: Session = Depends(get_db)):
    ambientes = crud.get_ambientes_por_tipo_de_circuito(db=db, tipo_circuito=tipo_circuito)
    if not ambientes:
        raise HTTPException(status_code=404, detail="No se encontraron ambientes para el tipo de circuito proporcionado.")
    return ambientes

# Endpoint para obtener dispositivos por fecha de instalación
@app.get("/dispositivos/fecha", response_model=List[schemas.Dispositivo])
def read_dispositivos_por_fecha_instalacion(fecha_inicio: Optional[date] = None, fecha_fin: Optional[date] = None, db: Session = Depends(get_db)):
    dispositivos = crud.get_dispositivos_por_fecha_instalacion(db=db, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    if not dispositivos:
        raise HTTPException(status_code=404, detail="No se encontraron dispositivos en el rango de fechas proporcionado.")
    return dispositivos

# Endpoint para obtener ocupación promedio
@app.get("/ocupacion/promedio/{ambienteid}", response_model=float)
def read_ocupacion_promedio(ambienteid: int, fecha_inicio: date, fecha_fin: date, db: Session = Depends(get_db)):
    ocupacion_promedio = crud.obtener_ocupacion_promedio(db=db, ambienteid=ambienteid, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)
    if ocupacion_promedio is None:
        raise HTTPException(status_code=404, detail="No se encontró ocupación promedio para el ambiente en el rango de fechas proporcionado.")
    return ocupacion_promedio

# Endpoint para obtener dispositivos de alto consumo
@app.get("/dispositivos/alto_consumo/{ambienteid}", response_model=List[schemas.Dispositivo])
def read_dispositivos_alto_consumo(ambienteid: int, consumo_minimo: float, db: Session = Depends(get_db)):
    dispositivos = crud.obtener_dispositivos_alto_consumo(db=db, ambienteid=ambienteid, consumo_minimo=consumo_minimo)
    if not dispositivos:
        raise HTTPException(status_code=404, detail="No se encontraron dispositivos con alto consumo para el ambiente proporcionado.")
    return dispositivos

# Endpoint para obtener subestaciones por nivel de tensión
@app.get("/subestaciones/nivel_tension/{nivel_tension_kva}", response_model=List[schemas.Subestacion])
def read_subestaciones_por_nivel_tension(nivel_tension_kva: float, db: Session = Depends(get_db)):
    subestaciones = crud.obtener_subestaciones_por_nivel_tension(db=db, nivel_tension_kva=nivel_tension_kva)
    if not subestaciones:
        raise HTTPException(status_code=404, detail="No se encontraron subestaciones para el nivel de tensión proporcionado.")
    return subestaciones
