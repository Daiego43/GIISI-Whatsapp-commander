import pandas as pd
import pyautogui as pg
import os

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"csv"}


def get_csv_fields(filename):
    """
    Receives the path to the current working file
    :param filename:
    :return:
    """
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
    return list(df.columns)


def wait_whatsapp_ready(path):
    loaded = False
    while not loaded:
        result1 = pg.locateOnScreen(os.path.join(path, "whatsappready.png"), confidence=0.9)
        result2 = pg.locateOnScreen(os.path.join(path, "whatsappready2.png"), confidence=0.9)
        result3 = pg.locateOnScreen(os.path.join(path, "whatsappready3.png"), confidence=0.9)
        print("Waiting for whatsapp web to show up")
        if (result1 is not None) or (result2 is not None) or (result3 is not None):
            print("Whatsapp web loaded")
            loaded = True


def locate_while(path, image, myconfidence=0.9):
    """
    This function will locate the center of an image on screen
    as soon as it finds it, will return those coordinates.
    :param myconfidence:
    :param path:
    :param image:
    :return:
    """
    loaded = False
    result = None
    while not loaded:
        result = pg.locateCenterOnScreen(os.path.join(path, image), confidence=myconfidence)
        print(f"locating {image}")
        if result is not None:
            print("found!")
            loaded = True
    return result


def clean_uploads():
    for file in os.listdir(UPLOAD_FOLDER):
        os.remove(os.path.join(UPLOAD_FOLDER, file))


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_uploaded_file():
    return os.path.join(UPLOAD_FOLDER, os.listdir(UPLOAD_FOLDER)[0])