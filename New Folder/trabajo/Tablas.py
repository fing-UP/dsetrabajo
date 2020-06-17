"""
BBDD's
- Carrito
- Cliente - Usuario - Persona
- Colaborador - Usuario
- Comercio
- DetalleCarrito o
- DetalleOrden
- Localizacion
- LocalizacionCliente
- Orden
- Repartidor - Persona o
- Producto
- TarjetaF

"""
# Conexión
import sqlite3
con = sqlite3.connect("linioexp_parcial_lab3.db")
cursor = con.cursor()
# Drop If Exist
cursor.execute("""
DROP TABLE IF EXISTS clientes""")
cursor.execute("""
DROP TABLE IF EXISTS productos""")
# ---------------------------------------------
# TABLA - CLIENTE
cursor.execute("""CREATE TABLE IF NOT EXISTS cliente(
    idCliente TEXT  PRIMARY KEY ,
    nombre TEXT NOT NULL,
    apellidoPaterno TEXT  NULL,
    apellidoMaterno TEXT  NULL,
    dni TEXT NOT NULL,
    fechaNacimiento DATE NULL,
    correo TEXT NULL,
    nombreUsuario TEXT  NULL,
    password TEXT  NULL,
    fechaRegistro DATETIME null,
    telefono INTEGER null,
    genero bool null

)""")
con.commit()
# DATOS CLIENTE

con.commit()
# ---------------------------------------------
# TABLA CATEGORIA

#cursor.execute("""CREATE TABLE IF NOT EXISTS categoria(
#    idCategoria TEXT PRIMARY KEY NOT NULL,
#    categoria varchar(30)
#)""")

#con.commit()
cursor.execute("""
CREATE TABLE IF NOT EXISTS comercio(
    idComercio TEXT  PRIMARY KEY ,
    ruc INT null,
    nombre VARCHAR(20) null
)""")
con.commit()

# TABLA PRODUCTO
cursor.execute("""CREATE TABLE IF NOT EXISTS producto(
    idProducto TEXT  PRIMARY KEY,
    nombre VARCHAR(250) NOT NULL,
    precio float NOT NULL,
    stock NUMERIC(0,10000) NOT NULL,
    descuento FLOAT NULL,
    categoria text null,
    idComercio TEXT FOREING KEY REFERENCES comercio(idComercio),
    descripcion TEXT
)""")
con.commit()
#idCategoria TEXT FOREING KEY REFERENCES categoria(idCategoria) NOT NULL

con.commit()
# ---------------------------------------------
# TABLA REPARTIDOR
cursor.execute("""
CREATE TABLE IF NOT EXISTS repartidor(
    idRepartidor TEXT  PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellidoPaterno TEXT NOT NULL,
    apellidoMaterno TEXT NOT NULL,
    dni TEXT NOT NULL,
    fechaIngreso DATETIME,
    fechaNacimiento DATETIME,
    genero bool
)""")

con.commit()
# ---------------------------------------------
# TABLA Tarjeta
cursor.execute(""" CREATE TABLE IF NOT EXISTS tarjeta(
   numTarjeta TEXT  PRIMARY KEY,
    idCliente TEXT FOREING KEY REFERENCES cliente(idCliente) null,
    proveedor TEXT NOT NULL,
    numSec TEXT NOT NULL,
    fechaVencimiento TEXT NOT NULL,
    nombrePropetario TEXT NOT NULL,
    preterminado bool    
)""")

con.commit()
#---------------------------------------------
# TABLA ORDEN
cursor.execute("""CREATE TABLE IF NOT EXISTS orden(
    idOrden TEXT PRIMARY KEY,
    idCliente TEXT FOREING KEY REFERENCES cliente(idCliente),
    idRepartidor TEXT  FOREING KEY REFERENCES repartidor(idRepartidor),
    idDireccionEntrega TEXT  FOREING KEY REFERENCES localizacionCliente(idLocalizacionCliente),
    metodoPago varchar(3) not null,
    numTarjeta TEXT  FOREING KEY REFERENCES tarjeta(numTarjeta),
    fechaRegistro date null,
    fechaEntrega date null,
    estado VARCHAR(30) NULL,
    tarifa float NULL
) """)

con.commit()
# ---------------------------------------------
# TABLA DETALLE ORDEN
cursor.execute("""
CREATE TABLE IF NOT EXISTS detalleOrden(
    idDetalleOrden TEXT PRIMARY KEY,
    idOrden INT FOREING KEY REFERENCES orden(idOrden),
    idProducto INT FOREING KEY REFERENCES producto(idProducto),
    cantidad INTEGER not null,
    subtotal FLOAT not null

)""")

con.commit()
# ---------------------------------------------
# TABLA COMERCIO

# ---------------------------------------------
# TABLA localaizacion
cursor.execute("""
CREATE TABLE IF NOT EXISTS localizacionComercio(
  idLocalizacionComercio TEXT PRIMARY KEY,
  idComercio TEXT FOREING KEY REFERENCES comercio(idComercio),
  provincia TEXT NOT NULL,
  distrito TEXT NOT NULL,
  codigoPostal TEXT NOT NULL,
  direccion TEXT NOT NULL,
  direccionSecundaria TEXT NOT NULL) """)

con.commit()

# ---------------------------------------------
# TABLA COLABORADOR
cursor.execute("""
CREATE TABLE IF NOT EXISTS colaborador(
    idColaborador TEXT  PRIMARY KEY,
    idComercio TEXT FOREING KEY REFERENCES comercio(idComercio) not null,
    nombreUsuario TEXT NOT NULL,
    password TEXT NOT NULL,
    fechaRegistro DATETIME,
    nombre TEXT NOT NULL,
    apellidoMaterno TEXT NOT NULL,
    apellidoPaterno TEXT NOT NULL,
    dni TEXT NOT NULL,
    correo TEXT NOT NULL,
    fechaNacimiento DATETIME,
    genero boll null
)""")
con.commit()

# ---------------------------------------------
# TABLA LOCALIZACIÓN Cliente
cursor.execute("""
CREATE TABLE IF NOT EXISTS localizacionCliente(
  idLocalizacionCliente TEXT PRIMARY KEY,
  idCliente TEXT FOREINGKEY REFERENCES cliente(idCliente),
  telefono INTEGER,
  nombre TEXT NOT NULL,
  apellidoPaterno TEXT NOT NULL,
  apellidoMaterno TEXT NOT NULL,
  preterminada BOOL NOT NULL,
  provincia TEXT NOT NULL,
  distrito TEXT NOT NULL,
  codigoPostal TEXT NOT NULL,
  direccion TEXT NOT NULL,
  direccionSecundaria TEXT NOT NULL
)""")

con.commit()
# ---------------------------------------------

#Carrito de Compras
cursor.execute(""" CREATE TABLE IF NOT EXISTS carrito(
    idCarrito TEXT  PRIMARY KEY,
    idCliente TEXT FOREING KEY REFERENCES cliente(idCliente),
    importeTotal INTEGER
)""")

# ----------------------------------------------------------------------------

con.commit()
# TABLA DETALLE CARRITO
cursor.execute(""" CREATE TABLE IF NOT EXISTS detalleCarrito(
    idDetalleCarrito TEXT PRIMARY KEY,
    idCarrito TEXT  FOREING KEY REFERENCES carrito(idCarrito) NOT NULL,
    idProducto TEXT FOREING KEY REFERENCES producto(idProducto) NOT NULL,
    cantidad INTEGER,
    subtotal INTEGER
)""")
# ---------------------------------------------
# Cerrar conexión
con.commit()
cursor.close()