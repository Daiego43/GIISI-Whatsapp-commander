import os
import pyautogui
from flask import *
from werkzeug.utils import secure_filename
from model.utilities import *
from model.create_group_chat import main as create_group_chat

app = Flask(__name__)
app.config['FILE_UPLOADS'] = os.path.join("uploads", "files")
app.config['IMAGE_UPLOADS'] = os.path.join("uploads", "images")


@app.route('/')
def home():  # put application's code here
    clean_uploads()
    return render_template("index.html")


@app.route('/group_creation', methods=['POST', "GET"])
def group_creation():
    error = [False, '']
    return render_template("group_chats_creation/form1_group_creation.html", error=error)


@app.route('/group_creation/process_contacts', methods=['POST', "GET"])
def process_file():
    """
    Validación de los campos del formulario
    Tiene pinta de que lo tengo fatal hecho pls help,
    Mejor que como lo tengo hecho, lo suyo sería hacer una funcion aparte que valide los campos del formulario
    :return:
    """
    error = [False, '']
    file = request.files['contacts']
    image = request.files['image']

    if file and allowed_file(file.filename):
        # Guardar el csv
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['FILE_UPLOADS'], filename))
        os.rename(os.path.join(app.config['FILE_UPLOADS'], filename),
                  os.path.join(app.config['FILE_UPLOADS'], "workingfile.csv"))

        # Guardar la imagen de grupo
        imagename = secure_filename(image.filename)
        image.save(os.path.join(app.config['IMAGE_UPLOADS'], imagename))
        name, extension = imagename.split('.')
        os.rename(os.path.join(app.config['IMAGE_UPLOADS'], imagename),
                  os.path.join(app.config['IMAGE_UPLOADS'], "workingimage."+extension))

        fields = get_csv_fields("workingfile.csv")
        creation_params = {"group_name": request.form['group_name'],
                           "file_path": get_uploaded_image(),
                           "image_path": get_uploaded_file()}
        return render_template("group_chats_creation/form2_group_creation.html", error=error, csv_fields=fields, creation_params=creation_params)
    else:
        error[0] = True
        if file.filename == '':
            error[1] = 'Archivo no subido'
        else:
            error[1] = 'Archivo no soportado, debe ser csv'
        return render_template("group_chats_creation/form1_group_creation.html", error=error)


@app.route("/group_creation/creating_the_group_finished", methods=['POST', "GET"])
def group_creation_finished():
    path_to_file = get_uploaded_file()
    path_to_image = get_uploaded_image()
    csv_field = request.form['field']
    group_name = request.form['group_name']
    create_group_chat(path_to_file, path_to_image,group_name, csv_field)
    msg = "Tu grupo se ha creado"
    return render_template("group_chats_creation/await_group_creation.html", message=msg)
