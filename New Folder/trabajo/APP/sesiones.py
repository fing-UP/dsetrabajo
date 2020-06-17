from flask import *
from Comercio import Comercio
from Colaborador import Colaborador
import datetime
from dateutil.relativedelta import relativedelta
from Carrito import Carrito
import os
from Cliente import Cliente
from DetalleCarrito import DetalleCarrito

template_dir = os.path.abspath('Templates/sesiones')
sesiones = Blueprint('sesiones', 'api', template_folder=template_dir)


from Producto import Producto



@sesiones.route('/iniciar')
def iniciar():
    return render_template('iniciar sesion.html',methods='POST')
@sesiones.route('/cerrarcuenta')
def cerrarcuenta():

    session['user_name'] = ""
    session["id"] = ""
    session["correo"] = ""
    return redirect(url_for("inicio.index"))

@sesiones.route('/iniciando',methods=['POST'])
def iniciando():
    if (request.method =='POST'):
        nombre=request.form['nombre']
        password = request.form['password']

        U=Cliente(password=password,correo=nombre,nombreusuario=nombre)
        if(U.iniciarSesion()==1):
            flash("sesion iniciada")

            session['user_name'] = U.nombreUsuario
            session["id"]=U.idCliente
            session["correo"]=U.correo
            try:
                for e in session["Carrito"]:
                    pre = Producto(idProducto=e[0])
                    pre.obtenerProducto()
                    Det = DetalleCarrito(
                    carrito=Carrito(idCarrito=Cliente(idCliente=session["id"]).generarListaCarrito()[0][0]),
                    cantidad=e[3], producto=pre)
                    print(4)
                    if (Det.obtenerDetalleCarrito() == 0):
                        print(Det.idDetalleCarrito,4)
                        Det.agregarDetalleCarrito()
                    else:
                        Det.cantidad=e[3]
                        Det.actualizarDetalleCarrito(var=1)
            except:
                pass
            session["Carrito"]=[]

            return redirect(url_for("inicio.index"))

        else:
            flash("datos incorrectos")
            return redirect(url_for("sesiones.iniciar"))
@sesiones.route('/registrate')
def registro():
    return render_template("registro.html")
@sesiones.route('/registrando',methods=['POST'])
def registrando():
    if (request.method=="POST"):
        nombre=request.form['nombre']
        apellidoPaterno = request.form['apellidoPaterno']
        apellidoMaterno = request.form['apellidoMaterno']
        correo = request.form['correo']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        fechaN = request.form['fechaN'].split("-")
        fechaN=datetime.date(int(fechaN[0]),int(fechaN[1]),int(fechaN[2]))
        print(fechaN)
        print(type(fechaN))
        password1 = request.form['password1']
        paasword2 = request.form['password2']
        genero=request.form['genero']
        print(Cliente().verificarUnique(usuario))
        if(password1==paasword2 and fechaN<datetime.date.today()-relativedelta(years=18) and Cliente().verificarUnique(usuario)==1 and Cliente().verificarUnique(correo)==1):
            Cli=Cliente(nombre=nombre,apellidoMaterno=apellidoMaterno,apellidoPaterno=apellidoPaterno,correo=correo,telefono=telefono,fechaNacimiento=fechaN,genero=genero,password=password1,nombreusuario=usuario)
            Cli.agregarCliente()
            Carrito(cliente=Cli).agregarCarrito()
            return redirect(url_for("inicio.index"))
        else:
            if(password1!=paasword2):
                flash("las claves no coinciden")
            elif(Cliente().verificarUnique(correo)==0):
                flash("este correo ya esta siendo utilizado")
            elif(Cliente().verificarUnique(fechaN)==0):
                flash("este usuario ya esta en uso")
            else:
                flash("debe ser mayor de edad")
            return redirect(url_for("sesiones.registro"))



@sesiones.route('/iniciandoc',methods=['POST'])
def iniciandoc():
    if (request.method =='POST'):
        nombre=request.form['nombre']
        password = request.form['password']

        U=Colaborador(password=password,correo=nombre,nombreusuario=nombre)
        if(U.iniciarSesion()==1):
            flash("sesion iniciada")

            session['user_namec'] = U.nombreUsuario
            session["idCol"]=U.idColaborador
            session["correoc"]=U.correo
            session["idCom"]=U.comercio.idComercio
            return redirect(url_for("comercio.ComProductos"))

        else:
            flash("datos incorrectos")
            return redirect(url_for("sesiones.iniciarc"))

@sesiones.route('/iniciarc')
def iniciarc():

    return render_template('ingresar.html',methods='POST')
@sesiones.route('/registrarComercio')
def registrarComercio():
    return render_template("registroComercio.html")
@sesiones.route('/registraComercio', methods=['POST'])
def registraComercio():
    if (request.method == 'POST'):
        global nombreC
        nombreC = request.form['nombre']
        global ruc
        ruc = request.form['ruc']

        return redirect(url_for("sesiones.registraColaborador"))

@sesiones.route('/registraColaborador')
def registraColaborador():
    return render_template("registroColaborador.html")
@sesiones.route('/registrarColaborador', methods=['POST'])
def registrarColaborador():
    if (request.method == "POST"):
        nombre = request.form['nombre']
        apellidoPaterno = request.form['apellidoPaterno']
        apellidoMaterno = request.form['apellidoMaterno']
        correo = request.form['correo']
        usuario = request.form['usuario']
        fechaN = request.form['fechaN']
        password1 = request.form['password1']
        paasword2 = request.form['password2']
        genero = request.form['genero']
        if session["idCom"]=="":
            comercio=Comercio(nombre=nombre,ruc=ruc)
            comercio.agregarComercio()
        else:
            comercio=Comercio(idComercio=session["idCom"])
            comercio.obtenerComercio()
        Co = Colaborador(nombre=nombre, apellidoMaterno=apellidoMaterno, apellidoPaterno=apellidoPaterno, correo=correo,
                       fechaNacimiento=fechaN, genero=genero, password=password1,
                      nombreusuario=usuario,comercio=comercio)
        Co.agregarcolaborador()
        return redirect(url_for("inicio.index"))