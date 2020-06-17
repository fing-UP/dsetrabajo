from flask import Blueprint, render_template, request
import os

template_dir = os.path.abspath('app/views')
sessions_page = Blueprint('sessions_page', 'api', template_folder=template_dir)

@sessions_page.route('/sign_in', methods=['GET'])
def new():
    return render_template('usuarios/welcome/index.html')