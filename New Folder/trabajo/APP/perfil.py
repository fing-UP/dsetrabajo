from flask import *
from Comercio import Comercio
from Colaborador import Colaborador

import datetime
from dateutil.relativedelta import relativedelta
from Tarjeta import Tarjeta
import os
from Cliente import Cliente
from flask_socketio import SocketIO, emit,send
template_dir = os.path.abspath('Templates/account')
account = Blueprint('account', 'api', template_folder=template_dir)

from Orden import Orden

@account.route('/perfil/datos')
def datos():
    cli=Cliente(idCliente=session["id"])
    cli.obtenerCliente()
    print(cli.idCliente)
    lista=[cli.nombre, cli.apellidoPaterno,cli.apellidoMaterno,cli.correo,str(cli.telefono),cli.nombreUsuario,cli.fechaNacimiento,cli.genero]
    print(lista[4],444)
    return render_template("datos.html",session=session["id"],cliente=lista)
@account.route('/actualizardatos',methods=['GET','POST'])
def actualizardatos():
    if (request.method=="POST"):
        nombre=request.form['nombre']
        apellidoPaterno = request.form['apellidoPaterno']
        apellidoMaterno = request.form['apellidoMaterno']
        correo = request.form['correo']
        telefono = request.form['telefono']
        usuario = request.form['usuario']
        fechaN = request.form['fechaN'].split("-")
        fechaN = datetime.date(int(fechaN[0]), int(fechaN[1]), int(fechaN[2]))
        print(fechaN)
        print(type(fechaN))
        print(type(fechaN))
        genero=request.form['genero']
        cli=Cliente(idCliente=session["id"])
        cli.obtenerCliente()
        if((cli.verificarUnique(variable=usuario)==1 and cli.verificarUnique(varaible=correo)==1) or (cli.nombreUsuario==usuario and cli.correo==correo) or (cli.nombreUsuario==usuario and cli.verificarUnique(variable=correo)==1) or (cli.verificarUnique(variable=usuario)==1 and cli.correo==correo)):
            print(11111111111111111)
            cli.nombre,cli.apellidoPaterno,cli.apellidoMaterno,cli.correo,cli.telefono,cli.nombreUsuario,cli.fechaNacimiento,cli.genero=nombre,apellidoPaterno,apellidoMaterno,correo,telefono,usuario,fechaN,genero
            cli.actualizarCliente()
            print(cli.fechaNacimiento)
        else:
            if(Cliente.verificarUnique(usuario)==0):
                flash("el usuario ya esta en uso")
            elif(Cliente().verificarUnique(correo)==0):
                flash("el correo ya esta en uso")
    return redirect(url_for("account.datos"))

@account.route('/perfil/tarjeta/actualizartarjeta')
def actualizartarjeta():
    user = None
    if (request.method == 'POST'):
        predeterminado = request.form('predeterminado')
        nombrePropietario = request.form('nombrePropietario')
        numSec = request.form('numSec')
        mesVencimiento = request.form('mesVencimiento')
        anoVencimiento = request.form('anoVencimiento')
        numTarjeta = request.form('numTarjeta')
        fechaVencimiento = mesVencimiento+'/'+anoVencimiento
        user = Tarjeta(nombrePropietario = nombrePropietario, numSec = numSec, fechaVencimiento = fechaVencimiento, numTarjeta = numTarjeta)
        user.actualizarTarjeta()

        if predeterminado:
            user().activarPredeterminado()
    return render_template('tarjetas.html', user = user)


@account.route('/perfil/tarjeta')
def tarjeta():
    tarjetas=Cliente(idCliente=session["id"]).generarListaTarjeta()
    print(tarjetas)
    preterminada=None

    con=0
    for x in range(len(tarjetas)):
        con+=1
        print(x)
        tarjetas[x]=tarjetas[x]+(Tarjeta(numTarjeta=tarjetas[x][0]).obtenerTarjetaOculta(),con,)
        print(tarjetas[x])
        if(tarjetas[x][6]==1):
            preterminada = tarjetas[x]
        

    try:
        tarjetas.remove(preterminada)
    except:
        pass
    preterminada= None if preterminada==[] else preterminada
    tarjetas.append(["","","","","","","","",100000])
    print(preterminada)
    return render_template("tarjetas.html",tarjetas=tarjetas,preterminada=preterminada)
@account.route('/Preterminada=<string:num>')
def Preterminada(num):
    tarjetas=Tarjeta(numTarjeta=num)
    tarjetas.obtenerTarjeta()
    tarjetas.activarPreterminado()
    return redirect(url_for("account.tarjeta"))


@account.route('/perfil/ordenes')
def ordenes():
    Ordenes = Cliente(idCliente=session["id"]).generarListaOrden()
    Ordenes.reverse()

    return render_template("ordenes.html", ordenes=Ordenes)
@account.route('/perfil/cancelando=<string:codigo>')
def cancelar(codigo):

    Orden(idOrden=codigo).cancelar_Orden()

    return redirect(url_for("account.ordenes"))
