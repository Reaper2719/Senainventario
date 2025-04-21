CREATE TYPE tipo_usuario_enum AS ENUM ('directivo', 'administrador', 'analista');

CREATE TABLE usuarios (
    userid SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    apellido VARCHAR(255),
    correo_electronico VARCHAR(255) UNIQUE,
    contrasena VARCHAR(255),
    tipo_de_usuario tipo_usuario_enum,
    CHECK (correo_electronico ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

CREATE TABLE regionales (
    regionalid VARCHAR(50) PRIMARY KEY, 
    nombre_de_la_region VARCHAR(255)   
);

CREATE TABLE centros (
    centroid VARCHAR(50) PRIMARY KEY,         
    nombre_del_centro VARCHAR(255),           
    ciudad VARCHAR(255),                      
    regionalid VARCHAR(50),                   
    FOREIGN KEY (regionalid) REFERENCES regionales (regionalid),
    UNIQUE (nombre_del_centro, regionalid)    
);

CREATE TABLE sedes (
    sedeid SERIAL PRIMARY KEY,
    nombre_de_la_sede VARCHAR(255), 
    direccion VARCHAR(255)          
);

CREATE TABLE sede_centro (
    sedeid INT,
    centroid VARCHAR(50),
    PRIMARY KEY (sedeid, centroid),
    FOREIGN KEY (sedeid) REFERENCES sedes (sedeid),
    FOREIGN KEY (centroid) REFERENCES centros (centroid)
);

CREATE TABLE ambientes (
    ambienteid SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    tipo_de_circuito VARCHAR(255),
    sedeid INT,
    FOREIGN KEY (sedeid) REFERENCES sedes (sedeid)
);

CREATE TABLE dispositivos (
    deviceid SERIAL PRIMARY KEY,
    nombre_del_dispositivo VARCHAR(255),
    descripcion TEXT,
    consumo_energetico FLOAT,
    fecha_de_instalacion DATE,
    ambienteid INT,
    FOREIGN KEY (ambienteid) REFERENCES ambientes (ambienteid),
    tipo_de_lugar VARCHAR(255),
    referencias_a_mediciones TEXT
);

CREATE TABLE ocupacion (
    ocupacionid SERIAL PRIMARY KEY,
    ambienteid INT,
    cantidad_de_personas INT,
    tiempo_de_ocupacion INTERVAL,
    fecha DATE,
    FOREIGN KEY (ambienteid) REFERENCES ambientes (ambienteid)
);

CREATE TABLE costos_energia (
    costoid SERIAL PRIMARY KEY,
    sedeid INT,
    ano INT,
    mes INT,
    fecha_inicio_factura DATE,
    fecha_fin_factura DATE,
    consumo_pkwh FLOAT,
    consumo_qvarh FLOAT,
    valor_factura FLOAT,
    contrato VARCHAR(255),
    cantidad_aprendices INT,
    cantidad_administrativos INT,
    FOREIGN KEY (sedeid) REFERENCES sedes (sedeid)
);

CREATE TABLE subestaciones (
    subestacionid SERIAL PRIMARY KEY,
    nombre_sub VARCHAR(255),
    sedeid INT,
    nivel_tension_kva FLOAT,
    FOREIGN KEY (sedeid) REFERENCES sedes (sedeid)
);
