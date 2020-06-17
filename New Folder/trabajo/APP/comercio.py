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
template_dir = os.path.abspath('Templates/Comercio')
comercio = Blueprint('comercio', 'api', template_folder=template_dir)
from Producto import Producto
from Colaborador import Colaborador
from Comercio import Comercio
import datetime
@comercio.route('/busqueda1',methods=['GET','POST'])
def busqueda1():
    busqueda=request.form['busqueda']
    print(3)
    categoria = request.form['categorias']
    print(categoria)
    return redirect("/Comercio/productos={}/{}/".format(busqueda,categoria))
@comercio.route('/Comercio/productos=/<string:cate>/',defaults={'name':-1,'page':-1})
@comercio.route('/Comercio/productos=<string:name>/<string:cate>/',defaults={'page':1})
@comercio.route('/Comercio/productos=<string:name>/<string:cate>/<int:page>')
@comercio.route('/Comercio/productos/<string:precio>/<string:orden>/<int:page>')
@comercio.route('/Comercio/productos=<string:name>/<string:cate>/<string:precio>/<string:orden>/<int:page>')
@comercio.route('/Comercio/productos/<int:page>',methods=['GET','POST'])
@comercio.route('/Comercio/productos/',methods=['GET','POST'])
def ComProductos(name=None,page=None,cate=None,precio=None,orden=None):
    if name != None and cate!=None:
        url='/Comercio/productos={}/{}/'.format(name,cate)
        if precio=="N-N" or precio==None:
            bajo=-1
            alto=10000000
        else:
            precio=precio.split("-")
            bajo=int(precio[0])
            alto=int(precio[1])
        alf="asc" if orden == "a-z" else "desc" if orden=="z-a" else None
        pre="asc" if orden == "asc" else "desc" if orden=="desc" else None


        print(name)
        if (cate == "todo"):
            listas = Producto().buscarProducto(Palabra=name, num=page,bajo=bajo,alto=alto,alf=alf,pre=pre)

        else:
            listas = Producto().buscarProducto(Palabra=name, num=page, categoria=[cate],bajo=bajo,alto=alto,alf=alf,pre=pre)

        for e in range(len(listas)):
            listas[e] += Producto(idProducto=listas[e][0]).CantidadVendidos()

            print(listas[e])
        return render_template("ProductosC.html", lista=listas,url=url)
    else:
        url = '/Comercio/productos/'
        if precio is None and orden is None:
            page= 1 if page is None else page

            listas = (Producto().buscarProducto(comercio=session["idCom"], Palabra="",num=page))

        else:
            if precio == "N-N" or precio == None:
                bajo = -1
                alto = 10000000
            else:
                precio = precio.split("-")
                bajo = int(precio[0])
                alto = int(precio[1])
            alf = "asc" if orden == "a-z" else "desc" if orden == "z-a" else None
            pre = "asc" if orden == "asc" else "desc" if orden == "desc" else None
            listas = (Producto().buscarProducto(comercio=session["idCom"], Palabra="", num=page,bajo=bajo,alto=alto,alf=alf,pre=pre))
        for e in range(len(listas)):
            listas[e] += Producto(idProducto=listas[e][0]).CantidadVendidos()

            print(listas[e])


        return render_template('ProductosC.html', lista=listas,url=url)
@comercio.route('/buscarFiltro1',methods=['GET','POST'])
def buscarFiltro1():
    filtro=""
    precioM=0
    preciom=0
    az=0
    za=0
    try:
        filtro=request.form["p"]
        preciom=1
    except:
        try:
            filtro = request.form["P"]
            precioM=1
        except:
            try:
                filtro = request.form["A"]
                az=1
            except:
                try:
                    filtro= request.form["Z"]
                    za=1
                except:
                    pass

    busqueda=request.form
    if(busqueda["minimo"]=='0' and busqueda["maximo"]=='1000000'):
        precio="N-N"
    else:
        precio="{}-{}".format(int(busqueda["minimo"]),int(busqueda["maximo"]))
    print(precio)
    print(busqueda,filtro)
    filtro="z-a" if za is 1 else "a-z" if az==1 else "desc" if precioM==1 else "asc" if preciom==1 else "-"
    try:
        int(busqueda["url"][-1])
        busqueda["url"] = busqueda["url"][:-1]
        url=busqueda["url"]+"{}/{}/1".format(precio,filtro)
    except:
        url = busqueda["url"] + "{}/{}/1".format(precio, filtro)
    print(url)



    return redirect(url)
"""        
@comercio.route('/Comercio/productos',methods=['GET','POST'])
def ComProductos():

    listas=(Producto().buscarProducto(comercio=session["idCom"],Palabra=""))
    for e in range (len(listas)):
        listas[e]+=Producto(idProducto=listas[e][0]).CantidadVendidos()

        print(listas[e])


    return render_template('ProductosC.html',lista=listas)"""
@comercio.route('/Comercio/AgegarProducto',methods=['GET','POST'])
def AgregarProducto():

    return render_template('agregarProducto.html')

@comercio.route('/Comercio/Comercio/agregandoProducto', methods=['GET', 'POST'])
def AgregandoProducto():
    print(44444444444444444444)

    if (request.method=="POST"):
        print(request.form)
        Nombre=request.form['nombre']
        Descripcion = request.form['Descripcion']
        Precio = request.form['Precio']
        Categoria = request.form['Categoria']
        Cantidad = request.form['Cantidad']
        Imagen = request.form['Imagen']
        Descuento = request.form['Descuento']
        co=Comercio(idComercio=session["idCom"])
        co.obtenerComercio()
        print(Categoria,33333333333)
        pro=Producto(nombre=Nombre,descuento=Descuento,categoria=Categoria,stock=Cantidad,precio=Precio,descripcion=Descripcion,comercio=co)
        pro.agregarProducto()
    return redirect(url_for("comercio.ComProductos"))
@comercio.route('/Comercio/ActualizarProducto=<string:productoc>',methods=['GET','POST'])
def ActualizarProducto(productoc):
    co=Comercio(idComercio=session["idCom"])
    productos=co.generarListaProductos()
    for e in productos:
        if productoc==e[0]:
            producto=e

    return render_template('modificarProducto.html',producto=producto)
@comercio.route('/Comercio/Comercio/AgctualizandoProducto=<string:producto>', methods=['GET', 'POST'])
def ActualizandoProducto(producto):


    if (request.method=="POST"):
        print(request.form)
        Nombre=request.form['nombre']
        Descripcion = request.form['Descripcion']
        Precio = request.form['Precio']
        Categoria = request.form['Categoria']
        Cantidad = request.form['Cantidad']
        Imagen = request.form['Imagen']
        Descuento = request.form['Descuento']
        co=Comercio(idComercio=session["idCom"])
        co.obtenerComercio()
        print(Categoria,33333333333)
        pro=Producto(idProducto=producto,nombre=Nombre,descuento=Descuento,categoria=Categoria,stock=Cantidad,precio=Precio,descripcion=Descripcion,comercio=co)
        pro.actualizarProducto()
    return redirect(url_for("comercio.ComProductos"))

@comercio.route('/Comercio/EliminarProducto=<string:producto>', methods=['GET', 'POST'])
def EliminarProducto(producto):


    pro=Producto(idProducto=producto)
    pro.obtenerProducto()
    if pro.oComercio.idComercio==session["idCom"]:
        pro.eliminarProducto()
    return redirect(url_for("comercio.ComProductos"))
@comercio.route('/Comercio/perfil/colaboradores')
def ordenes():
    Ordenes = Comercio(idComercio=session["idCom"]).generarListaColaboradores()
    Ordenes.reverse()

    return render_template("colaboradores.html", ordenes=Ordenes)
@comercio.route('/Comercio/perfil/datos')
def datos():
    cli=Colaborador(idColaborador=session["idCol"])
    cli.obtenercolaborador()
    print(cli.idColaborador,cli.nombre)

    lista=[cli.nombre, cli.apellidoPaterno,cli.apellidoMaterno,cli.correo,cli.nombreUsuario,cli.fechaNacimiento,cli.genero]
    print(cli.fechaNacimiento)

    return render_template("datosC.html",session=session["id"],cliente=lista)
@comercio.route('/Comercio/actualizardatos',methods=['GET','POST'])
def actualizardatos():
    if (request.method=="POST"):
        nombre=request.form['nombre']
        apellidoPaterno = request.form['apellidoPaterno']
        apellidoMaterno = request.form['apellidoMaterno']
        correo = request.form['correo']

        usuario = request.form['usuario']
        fechaN = request.form['fechaN'].split("-")
        fechaN = datetime.date(int(fechaN[0]), int(fechaN[1]), int(fechaN[2]))

        genero=request.form['genero']

        cli=Colaborador(idColaborador=session["idCol"])
        print(3333)
        cli.obtenercolaborador()
        if((cli.verificarUnique(variable=usuario)==1 and cli.verificarUnique(varaible=correo)==1) or (cli.nombreUsuario==usuario and cli.correo==correo) or (cli.nombreUsuario==usuario and cli.verificarUnique(variable=correo)==1) or (cli.verificarUnique(variable=usuario)==1 and cli.correo==correo)):
            print(11111111111111111)
            cli.nombre,cli.apellidoPaterno,cli.apellidoMaterno,cli.correo,cli.nombreUsuario,cli.fechaNacimiento,cli.genero=nombre,apellidoPaterno,apellidoMaterno,correo,usuario,fechaN,genero

            cli.actualizarcolaborador()
            print(cli.fechaNacimiento)
        else:
            if(Cliente.verificarUnique(usuario)==0):
                flash("el usuario ya esta en uso")
            elif(Cliente().verificarUnique(correo)==0):
                flash("el correo ya esta en uso")
    return redirect(url_for("comercio.datos"))