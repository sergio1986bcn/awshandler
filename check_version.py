#!/usr/bin/python3

import requests
import time


version = 'v0.0.1'


def check():
    # Consulto los realease
    response = requests.get("https://api.github.com/repos/sergio1986bcn/awshandler/releases")
    releases = response.json()

    # Último release
    latest_release = releases[0]['tag_name']

    if latest_release:
        # Quito la "v" de las versiones y convierto el número en entero
        version_number = list(map(int, version.split('v')[-1].split('.')))
        latest_release_number = list(map(int, latest_release.split('v')[-1].split('.')))

        if version_number < latest_release_number:
            print("¡¡Hay una nueva realease disponible!!")
            time.sleep(1)
