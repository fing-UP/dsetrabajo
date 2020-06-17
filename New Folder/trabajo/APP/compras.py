from flask import *
from Producto import Producto
from Cliente import Cliente
from DetalleCarrito import DetalleCarrito
from Carrito import Carrito
from Producto import Producto
from Tarjeta import Tarjeta
from Cliente import Cliente
from LocalizacionCliente import LocalizacionCliente

import os
from Cliente import Cliente
template_dir = os.path.abspath('Templates/compras')
compras = Blueprint('compras', 'api', template_folder=template_dir)



@compras.route('/carrito',methods=['GET','POST'])
def carrito():

    session["selel"] = ""

    session["selet"] = ""
    print(session["id"]!="")
    if session["id"] != None and session["id"] != "":
        try:
            listas=Carrito(idCarrito=Cliente(idCliente=session["id"]).generarListaCarrito()[0][0]).generarListaDetalleCarrito()


            listas=[tuple(Producto(idProducto=x[2]).obtenerlistaProducto())+x for x in listas]

        except:
            listas=[]

    else:
        try:
            listas=[tuple(Producto(idProducto=x[0]).obtenerlistaProducto())+tuple(x) for x in session["Carrito"]]
        except:
            listas=[]
    p=0 if session["id"]== "" or session["id"] is None else 1
    return render_template('carrito.html',lista=listas,session=p)
@compras.route('/anadir=<string:codigo>',methods=['GET','POST'])
@compras.route('/anadir',methods=['GET','POST'])

def anadir(codigo=None):
    if (request.method =='POST' or codigo is not None):
        if codigo is None:
            idproducto = request.form['idproducto']

            number = int(request.values['number'])
        else:
            idproducto=codigo
            number=1

        if session["id"] != "" and session["id"]!= None:
            print(session["id"], 4343)
            pre=Producto(idProducto=idproducto)
            pre.obtenerProducto()

            Det=DetalleCarrito(carrito=Carrito(idCarrito=Cliente(idCliente=session["id"]).generarListaCarrito()[0][0]),cantidad=number,producto=pre)

            if(Det.obtenerDetalleCarrito()==0):
                print(Det.idDetalleCarrito,Det)
                Det.agregarDetalleCarrito()
            else:
                Det.cantidad=number
                Det.actualizarDetalleCarrito(var=1)

        else:
            t=1
            try:

                c=0
                for e in session["Carrito"] :
                    if (e[0]==idproducto):
                        session["Carrito"][c][3]+=number
                        session.modified=True
                        t=t*0
                        c+=1

            except:
                print(t)
                session["Carrito"]=[]
                session.modified=True
            print(t)
            if (session["Carrito"])==[]:
                t=1
            print(session["Carrito"])
            print(4)
            if t==1 :
                print(4)
                session["Carrito"].append([idproducto,0,0,number,0])
                session.modified = True



    return redirect(url_for("compras.carrito"))
@compras.route('/<string:codigo>',methods=['GET','POST'])
def actualizar(codigo):
    cod=codigo[0:(len(codigo)-1)] if codigo[-1]=="+" or codigo[-1]=="-" else codigo
    if session["Carrito"]==[]:
        det=DetalleCarrito(idDetallecarrito=cod)
        det.obtenerDetalleCarrito()


    if(codigo[-1]=="-"):
        if session["Carrito"]==[]:
            if det.cantidad>1:
                det.disminuirCantidad(1)
        else:
            print(5)
            c = 0
            for e in session["Carrito"]:
                print(cod,e[0],c)
                if (e[0] ==cod):
                    print(5)
                    print(session["Carrito"][c])
                    if (session["Carrito"][c][3] > 1):
                        session["Carrito"][c][3] -=1
                        session.modified=True
                        print(session["Carrito"][c])
                c += 1
        return redirect(url_for("compras.carrito"))
    elif(codigo[-1]=="+"  ):

        if session["Carrito"]==[]:
            det.aumentarCantidad(1)
        else:
            c = 0
            for e in session["Carrito"]:
                if (e[0] ==cod):
                    session["Carrito"][c][3] +=1
                    session.modified=True
                c += 1
        return redirect(url_for("compras.carrito"))
    elif(codigo[-1]== "e"):
        if session["Carrito"]==[]:
            print(det.idDetalleCarrito)
            det.eliminarDetalleCarrito()
        else:
            c = 0
            for e in session["Carrito"]:
                if (e[0] ==cod):
                    session["Carrito"].remove(session["Carrito"][c])
                    session.modified=True
                c+=1
        return redirect(url_for("compras.carrito"))
    return redirect(url_for('inicio.index'))


@compras.route('/procesarCompra<int:codigo>',methods=['GET','POST'])
def procesarCompra(codigo):
    if codigo is 0:
        print(3)
        return redirect(url_for("sesiones.iniciar"))
    else:

        if DetalleCarrito().verificarstock(idC=session["id"]):
            return redirect(url_for("compras.configuracionCompra"))
        else:
            flash("Productos sin stock")
            return redirect(url_for("compras.carrito"))
@compras.route('/configuracionCompra',methods=['GET','POST'])
def configuracionCompra():
    if (request.method == 'POST'):
        pass
    else:


        print(session["selet"])
        Cli=Cliente(idCliente=session["id"])
        print(session["id"])

        if session["selet"]=="":
            print(2)
            Tar = [y if y[6]==1 else "" for y in Cli.generarListaTarjeta()]

            for e in range(len(Tar)):
                try:
                    Tar.remove("")
                except:
                    pass
            Tar[0] += (Tarjeta(numTarjeta=Tar[0][0]).obtenerTarjetaOculta(),)
        else:

            Tar = [y if str(y[0]) == str(session["selet"]) else "" for y in Cli.generarListaTarjeta()]
            print(Tar)
            for e in range(len(Tar)):
                try:
                    Tar.remove("")
                except:
                    pass
            Tar[0] += (Tarjeta(numTarjeta=str(session["selet"])).obtenerTarjetaOculta(),)
        if session["selel"]=="":
            Loca = [x if x[6] == 1 else "" for x in Cli.generarListaLocalizacion()]
            Loca.remove("")
            for e in range(len(Loca)):
                try:
                    Loca.remove("")
                except:
                    pass
        else:
            Loca = [x if x[0] == session["selel"] else "" for x in Cli.generarListaLocalizacion()]
            Loca.remove("")
            for e in range(len(Loca)):
                try:
                    Loca.remove("")
                except:
                    pass



        print(Loca,Tar)
        Car=Carrito(idCarrito=Cli.generarListaCarrito()[0][0])
        Car.obtenerCarrito()

        Total=float(Car.importeTotal)
        envio= 5 if Total*0.03<5 else int(Total*0.02)


    return render_template("opcioncompra.html",localizacion=Loca[0],tarjeta=Tar[0],Total=Total,envio=envio)
@compras.route('/TerminandoCompra',methods=['GET','POST'])

def terminadoCompra():
    if DetalleCarrito().verificarstock(idC=session["id"]):

        if (request.method == 'POST') :

            re = request.form
            tar = Tarjeta(numTarjeta=re["cod"])
            loc = LocalizacionCliente(idLocalizacionCliente=re["cod1"])
            loc.obtenerLocalizacionCliente()
            tar.obtenerTarjeta()
            print(session["id"])
            Cli = Cliente(idCliente=session["id"])
            Cli.obtenerCliente()
            print(23241)
            Car = Carrito(idCarrito=Cli.generarListaCarrito()[0][0])
            Car.obtenerCarrito()
            Car.comprarCarrito(Lugar=loc,tarjeta=tar)
            print("comprado")


        return redirect(url_for('inicio.index'))
    else:
        flash("El proveedor se quedo sin stock")
        return redirect(url_for('compras.carrito'))

@compras.route('/seleccionar',methods=['GET','POST'])
def seleccionar():
    tarjetas = Cliente(idCliente=session["id"]).generarListaTarjeta()
    preterminada = None
    print(tarjetas)
    con = 0
    for x in range(len(tarjetas)):
        con += 1
        print(x)
        tarjetas[x] = tarjetas[x] + (Tarjeta(numTarjeta=tarjetas[x][0]).obtenerTarjetaOculta(), con,)
        print(tarjetas[x])
        if (tarjetas[x][6] == 1):
            preterminada = tarjetas[x]

    try:
        tarjetas.remove(preterminada)
    except:
        pass

    return render_template("tarjetassele.html", tarjetas=tarjetas, preterminada=preterminada)

@compras.route('/seleccionarl',methods=['GET','POST'])
def seleccionarl():
    loca= Cliente(idCliente=session["id"]).generarListaLocalizacion()
    preterminada = None
    con = 0
    for x in range(len(loca)):
        con += 1
        print(x)
        print(loca[x])
        if (loca[x][6] == 1):
            preterminada = loca[x]

    try:
        loca.remove(preterminada)
    except:
        pass
    print(preterminada,loca)

    return render_template("localizacion.html", localizacion=loca, preterminada=preterminada)
@compras.route('/selecionando<string:codigo>',methods=['GET','POST'])
def selecionando(codigo=None):
    if (request.method == 'POST'):
        pass
    else:
        try:
            if codigo[0]=="L":
                session["selel"]=codigo
        except:
            session["selel"]=""
        try:

            codigo=int(codigo)

            session["selet"]=codigo
        except:
            session["selet"]=""
    return redirect(url_for('compras.configuracionCompra'))