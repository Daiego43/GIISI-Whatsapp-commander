import pyautogui as pag
import pandas as pd
import webbrowser as web
import pyperclip
import os
from model.utilities import wait_whatsapp_ready, locate_while

path_to_images_group = "static/images/group_creation"
path_to_images = "static/images"


class GroupChats:
    def __init__(self, chat_members, group_name, photo_path, sleep_time=1.0):
        pag.MINIMUM_SLEEP = sleep_time
        self.group_members = chat_members
        self.group_name = group_name
        self.group_photo = photo_path

    def step_1(self):
        # Hacer click en menú
        pag.press('tab')
        pag.press('tab')
        pag.press('tab')
        pag.press('enter')

    def step_2(self):
        pag.press("down")
        pag.press("enter")
        pag.sleep(pag.MINIMUM_SLEEP)

    def step_3(self):
        # Ingresar los contactos
        erase = 0
        for contact in self.group_members:
            pag.write(contact)
            pag.press("enter")
            pag.sleep(pag.MINIMUM_SLEEP)

    def step_4(self):
        # Continuar
        x, y = locate_while(path_to_images_group, "step_4.jpeg")
        pag.moveTo(x, y)
        pag.click()
        pag.sleep(pag.MINIMUM_SLEEP)

    def step_5(self):
        # Nombre para el grupo
        pag.write(self.group_name)
        # Poner la imagen
        x, y = locate_while(path_to_images_group, "step_5.png")
        pag.moveTo(x, y)
        pag.click()
        for _ in range(2): pag.press("down")
        pag.press("enter")
        # uploads/images/step_6.png
        pyperclip.copy(os.path.abspath(self.group_photo))
        pag.sleep(1.5)
        pag.hotkey("ctrl", "v")
        pag.sleep(1.5)
        pag.press("enter")
        pag.sleep(1.5)
        pag.press("tab")
        pag.press("tab")
        pag.press("tab")
        pag.press("tab")
        pag.press("tab")
        pag.press("enter")
        pag.sleep(pag.MINIMUM_SLEEP)

    def create_group_chat(self):
        if self.group_members:
            # Hacer click en menú
            print("step 1")
            self.step_1()
            # Hacer click en nuevo grupo
            print("step 2")
            self.step_2()
            # Añadir a los integrantes del chat
            print("step 3")
            self.step_3()
            # Continuar
            print("step 4")
            self.step_4()
            # Poner imagen y nombre
            print("step 5")
            self.step_5()


def main(file_path, photo_path, group_name, csv_field, sleep_time=1):
    web.open("https://web.whatsapp.com/", new=True)
    df = pd.read_csv(file_path)
    chat_members = list(df[csv_field])
    wait_whatsapp_ready(path_to_images)
    c = GroupChats(chat_members, group_name, photo_path, sleep_time)
    c.create_group_chat()


if __name__ == "__main__":
    main(sleep_time=0.5)
