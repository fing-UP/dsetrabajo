from flask import *
from Producto import Producto

import os
from Cliente import Cliente
template_dir = os.path.abspath('Templates/productos')
print(template_dir)
productos = Blueprint('productos', 'api', template_folder=template_dir)


@productos.route('/busqueda',methods=['GET','POST'])
def busqueda():
    busqueda=request.form['busqueda']
    print(3)
    categoria = request.form['categorias']
    print(categoria)
    return redirect("/buscar={}/{}/".format(busqueda,categoria))
@productos.route('/buscar=/<string:cate>/',defaults={'name':-1,'page':-1})
@productos.route('/buscar=<string:name>/<string:cate>/',defaults={'page':1})
@productos.route('/buscar=<string:name>/<string:cate>/<int:page>')
@productos.route('/buscar=<string:name>/<string:cate>/<string:precio>/<string:orden>/<int:page>')
def buscar(name,page,cate,precio=None,orden=None):
    url='/buscar={}/{}/'.format(name,cate)
    if precio=="N-N" or precio==None:
        bajo=-1
        alto=10000000
    else:
        precio=precio.split("-")
        bajo=int(precio[0])
        alto=int(precio[1])
    alf="asc" if orden == "a-z" else "desc" if orden=="z-a" else None
    pre="asc" if orden == "asc" else "desc" if orden=="desc" else None
    if (name == -1):
        return redirect(url_for("inicio.index"))
    else:
        print(name)
        if (cate == "todo"):
            productos = Producto().buscarProducto(Palabra=name, num=page,bajo=bajo,alto=alto,alf=alf,pre=pre)

        else:
            productos = Producto().buscarProducto(Palabra=name, num=page, categoria=[cate],bajo=bajo,alto=alto,alf=alf,pre=pre)

        return render_template("buscar.html", products=productos,url=url)

@productos.route('/producto=<string:name>')
def producto(name):
    print(name)
    pr=Producto(idProducto=name)
    pr.obtenerProducto()


    return render_template("producto.html",idproducto=pr.idProducto,nombre=pr.nombre,precio=pr.precio,session=session["id"])

@productos.route('/buscarFiltro',methods=['GET','POST'])
def buscarFiltro():
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