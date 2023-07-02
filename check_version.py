#!/usr/bin/python3

import requests

version = 'v0.1.0'

def check_version():
    response = requests.get(f"https://api.github.com/repos/sergio1986bcn/awshandler/releases")
    releases = response.json()
    
    latest_release = releases[0]  # La API de GitHub devuelve las releases en orden, con la más reciente primero
    print(latest_release['tag_name'])

check_version()