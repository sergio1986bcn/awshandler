#!/usr/bin/python3

import requests
import time


version = 'v0.0.1'


def check():
    # Consulto los realease
    response = requests.get(
        "https://api.github.com/repos/sergio1986bcn/awshandler/releases"
    )
    releases = response.json()

    # Último release
    latest_release = releases[0]['tag_name']

    print (latest_release[0]['assets'])

    if version < latest_release:
        mensaje = input ("¡¡Hay una nueva realease disponible!! ¿Quieres actualizar? [S/n]")
        
        if mensaje in ['S', 's']:
            zipball_url = releases[0]['assets']['zipball_url']
            response = requests.get(zipball_url)
        elif mensaje in ['N', 'n']:
            exit()
