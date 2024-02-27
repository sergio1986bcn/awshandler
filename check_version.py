#!/usr/bin/python3

import requests
import zipfile
import io
import configparser
from settings import config_file

parser = configparser.ConfigParser()

version = 'v0.1.0'


def check():

    parser.read(config_file)

    if parser['default'].getboolean('check_update', fallback=False):
        # Consulto los realease
        response = requests.get(
            "https://api.github.com/repos/sergio1986bcn/awshandler/releases"
        )
        releases = response.json()

        # Último release
        latest_release = releases[0]['tag_name']

        if version < latest_release:
            mensaje = input ("¡¡Hay una nueva realease disponible!! ¿Quieres actualizar? [S/n]")
            
            if mensaje in ['S', 's']:
                # Obtiene la url del artefacto
                zipball_url = releases[0].get("zipball_url")
                # Descarga el archivo
                response = requests.get(zipball_url)
                # Crea un objeto de archivo zip en memoria a partir de los datos descargados
                zip_data = io.BytesIO(response.content)
                with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                    # Especifica la ubicación donde deseas extraer los archivos
                    extract_path = "" 
                    zip_ref.extractall(extract_path)

            elif mensaje in ['N', 'n']:
                exit()
