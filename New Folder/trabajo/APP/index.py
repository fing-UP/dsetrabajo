from flask import *

import os
from Cliente import Cliente
template_dir = os.path.abspath('trabajo/Templates')

inicio = Blueprint('inicio', 'api', template_folder=template_dir)

@inicio.route('/')
def index():



    try:
        cliente=session['id']

        CLI=Cliente(idCliente=cliente)
        CLI.obtenerCliente()
        usuario=str(CLI.nombre)
    except:
        session['id']=""

    return render_template('index.html')


