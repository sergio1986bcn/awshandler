#!/usr/bin/python3

import requests


def check_update():
    response = requests.get(f"https://api.github.com/repos/sergio1986bcn/awshandler/releases")
    releases = response.json()
    
    latest_release = releases[0]  # La API de GitHub devuelve las releases en orden, con la más reciente primero
    print(latest_release['name'])

# def update():
#     if latest_version is not None and latest_version != main.version:
#         print(f"Hay una nueva versión disponible: {latest_version}")
#         if input("¿Quieres actualizar? (S/N) "):
#             subprocess.run(["git", "pull"])
#             print("El código se ha actualizado. El script se cerrará.")
#             sys.exit()

check_update()