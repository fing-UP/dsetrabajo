from flask import Blueprint, render_template, request
import os

template_dir = os.path.abspath('app/views')
print(template_dir)
registration_page = Blueprint('registration_page', 'api', template_folder=template_dir)

@registration_page.route('/sign_up', methods=['GET'])
def new():
    return render_template('usuarios/registrations/new.html')