from settings import aws_credentials_file, aws_config_file, config_file
from logger import logger
import aws_mfa

import configparser
import re
import os
from simple_term_menu import TerminalMenu
import boto3
import botocore.exceptions
import time

parser = configparser.ConfigParser()


def add():
    # Datos necesarios
    name = input("Introduce el nombre del perfil: ")
    account = input("Introduce el número de cuenta AWS: ")
    role = input("Introduce el nombre del role de salto: ")
    source = input("Introduce el origen del salto: ")
    region = input("Introduce la region: ")
    role_session_name = input("Introduce tu nombre de usuario AWS: ")

    # Valida si el origen del salto existe
    if f'[{source}]' in open(aws_credentials_file).read() or "mfa" in source:

        role_arn = f'arn:aws:iam::{account}:role/{role}'

        parser.clear()
        parser.read(aws_config_file)
        parser[f'profile {name}'] = {
            'role_arn': role_arn,
            'source_profile': source,
            'region': region,
            'role_session_name': role_session_name
        }
        with open(aws_config_file, 'w') as configfile:
            parser.write(configfile)

    else:
        print('\n')
        input("El origen de los datos no existe... Pulsa cualquier tecla para volver al menú principal...")


def list():
    with open(aws_config_file, 'r') as infile:
        for line in infile:
            res = re.findall(r"\[profile ([\w-]+)\]", line)
            if res:
                print(" ".join(res))
        print('\n')
        input("Pulsa cualquier tecla para volver al menú principal...")


def select():

    profiles = []

    with open(aws_config_file, 'r') as infile:
        for line in infile:
            res = re.findall(r"\[profile ([\w-]+)\]", line)
            if res:
                profiles.append(res[0])

    menu_entry_index = TerminalMenu(profiles).show()

    # Guardo el perfil seleccionado en el archivo de configuración
    parser.clear()
    parser.read(config_file)
    parser.set('general', 'profile', profiles[menu_entry_index])
    with open(config_file, 'w') as configfile:
        parser.write(configfile)

    # Leo el archivo config de aws para extraer el valor de rolearn y session iam
    parser.clear()
    parser.read(aws_config_file)
    rolearn = parser['profile ' + profiles[menu_entry_index]]['role_arn']
    session_name = parser['profile ' + profiles[menu_entry_index]]['role_session_name']

    while True:
        try:
            # Solicito credenciales temporales de CLI del profile seleccionado
            session = boto3.Session(profile_name="mfa")
            sts = session.client("sts")
            response = sts.assume_role(
                RoleArn=rolearn,
                RoleSessionName=session_name
            )
            break
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'ExpiredToken':
                logger.error("Token expirado: %s", e)
                os.system("clear")
                print("El token de seguridad ha expirado... Introdúcelo de nuevo...")
                time.sleep(2)
                os.system("clear")
                aws_mfa.check()

            else:
                print("Error al asumir el role...")
                logger.error("Error al asumir el role: %s", e)

    # Inserto en el archivo credentials el usuario y contraseña temporal de CLI del profile seleccionado
    parser.clear()
    parser.read(aws_credentials_file)
    parser['default'] = {
        'aws_access_key_id': response['Credentials']['AccessKeyId'],
        'aws_secret_access_key': response['Credentials']['SecretAccessKey'],
        'aws_session_token': response['Credentials']['SessionToken'],
    }
    with open(aws_credentials_file, 'w') as configfile:
        parser.write(configfile)
