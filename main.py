#!/usr/bin/python3

from simple_term_menu import TerminalMenu
import signal
import sys
import os
import getpass
import re
import boto3
import time
import configparser
from pathlib import Path
import logging
import botocore.exceptions

import check_version
import login_ecr

# Variables globales
home = str(Path.home())
parser = configparser.ConfigParser()

# Ruta absoluta del directorio donde se encuentra el script
dir_path = os.path.dirname(os.path.realpath(__file__))

config_file = os.path.join(dir_path, 'config.ini')

aws_credentials_file = home + "/.aws/credentials"
aws_config_file = home + "/.aws/config"

# Configura el registro
logging.basicConfig(
    filename=os.path.join(dir_path, 'error.log'),
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)


def clear_screen():
    os.system('clear')


def aws_add_credentials():

    project = input("Introduce el nombre del proyecto: ")
    access_key = input("Introduce AWS access key: ")
    secret_key = getpass.getpass("Introduce AWS secret key: ")
    region = input("Introduce la región: ")

    parser.clear()
    parser.read(aws_credentials_file)
    parser[project] = {
        'aws_access_key_id': access_key,
        'aws_secret_access_key': secret_key
    }
    with open(aws_credentials_file, 'w') as configfile:
        parser.write(configfile)

    parser.clear()
    parser.read(aws_config_file)
    parser[project] = {
        'region': region
    }
    with open(aws_config_file, 'w') as configfile:
        parser.write(configfile)


def aws_add_profiles():
    # Datos necesarios
    name = input("Introduce el nombre del perfil: ")
    role = input("Introduce el arn del role de salto: ")
    source = input("Insstroduce el origen del salto: ")
    region = input("Introduce la region: ")
    role_session_name = input("Introduce tu nombre de usuario AWS: ")

    # Valido si el origen del salto existe para insertar los datos en el archivo config
    if '[' + source + ']' in open(aws_credentials_file).read() or "mfa" in source:

        parser.clear()
        parser.read(aws_config_file)
        parser['profile ' + name] = {
            'role_arn': role,
            'source_profile': source,
            'region': region,
            'role_session_name': role_session_name
        }
        with open(aws_config_file, 'w') as configfile:
            parser.write(configfile)

    else:
        print('\n')
        input("El origen de los datos no existe... Pulsa cualquier tecla para volver al menú principal...")


def aws_list_credentials():
    with open(aws_credentials_file, 'r') as infile:
        for line in infile:
            res = re.findall(r"\[([\w-]+)\]", line)
            if res:
                print(" ".join(res))
        print('\n')
        input("Pulsa cualquier tecla para volver al menú principal...")


def aws_list_profiles():
    with open(aws_config_file, 'r') as infile:
        for line in infile:
            res = re.findall(r"\[profile ([\w-]+)\]", line)
            if res:
                print(" ".join(res))
        print('\n')
        input("Pulsa cualquier tecla para volver al menú principal...")


def aws_select_credentials():

    profiles = []

    with open(aws_credentials_file, 'r') as infile:
        for line in infile:
            res = re.findall(r"\[([\w-]+)\]", line)
            if res:
                profiles.append(res[0])

    menu_entry_index = TerminalMenu(profiles).show()

    # Guardo el perfil seleccionado en el archivo de configuración
    parser.clear()
    parser.read(config_file)
    parser.set('general', 'account', profiles[menu_entry_index])
    with open(config_file, 'w') as configfile:
        parser.write(configfile)


def aws_mfa():
    # Leo el archivo de configuración para extraer el valor de account
    parser.clear()
    parser.read(config_file)
    credentials = parser['general']['account']

    # Con la variable credentials extraigo access y secret key de la account
    parser.clear()
    parser.read(aws_credentials_file)
    aws_access_key_id = parser[credentials]['aws_access_key_id']
    aws_secret_access_key = parser[credentials]['aws_secret_access_key']

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )
    iam = session.client('iam')
    sts = session.client('sts')

    username = iam.get_user()["User"]["UserName"]
    arn_mfa = iam.list_mfa_devices(UserName=username)['MFADevices']

    if len(arn_mfa) > 1:
        mfa_device_arns = [device['SerialNumber'] for device in arn_mfa]
        terminal_menu = TerminalMenu(
            mfa_device_arns,
            title="Selecciona el MFA que quieres utilizar:\n"
        )
        selected_device_index = terminal_menu.show()
        arn_mfa = mfa_device_arns[selected_device_index]
    else:
        arn_mfa = arn_mfa[0]['SerialNumber']

    # Guardo el mfa seleccionado en el archivo de configuración
    parser.clear()
    parser.read(config_file)
    parser.set('general', 'mfa', arn_mfa)
    with open(config_file, 'w') as configfile:
        parser.write(configfile)

    while True:
        mfa = input("Ingrese el código MFA: ")
        if len(mfa) != 6:
            logging.error("El código MFA ingresado no tiene 6 dígitos --- %s", mfa)
            os.system("clear")
            print("El código MFA ingresado no tiene 6 dígitos...")
            time.sleep(2)
            os.system("clear")
        else:
            try:
                credentials_mfa = sts.get_session_token(
                    DurationSeconds=43200,
                    SerialNumber=arn_mfa,
                    TokenCode=mfa
                )
                break
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'AccessDenied':
                    logging.error("Error en el código MFA ingresado: %s", e)
                    os.system("clear")
                    print("Has introducido mal el MFA, inténtalo de nuevo.")
                    time.sleep(2)
                    os.system("clear")
                else:
                    print("Error al obtener las credenciales MFA")
                    logging.error("Error al obtener las credenciales MFA: %s", e)

    parser.clear()
    parser.read(aws_credentials_file)
    parser['mfa'] = {
        'aws_access_key_id': credentials_mfa['Credentials']['AccessKeyId'],
        'aws_secret_access_key': credentials_mfa['Credentials']['SecretAccessKey'],
        'aws_session_token': credentials_mfa['Credentials']['SessionToken'],
    }
    parser['default'] = {
        'aws_access_key_id': credentials_mfa['Credentials']['AccessKeyId'],
        'aws_secret_access_key': credentials_mfa['Credentials']['SecretAccessKey'],
        'aws_session_token': credentials_mfa['Credentials']['SessionToken'],
    }

    with open(aws_credentials_file, 'w') as configfile:
        parser.write(configfile)

    # Extraigo y formateo la fecha y hora de la expiración del token MFA solicitado
    expiration_token = credentials_mfa['Credentials']['Expiration']
    expiration_token_str = expiration_token.strftime('%d-%m-%Y %H:%M:%S')

    # Guardo la fecha y hora de la expiración del token MFA solicitado en el archivo de configuración
    parser.clear()
    parser.read(config_file)
    parser.set('general', 'mfa_expiration', expiration_token_str)
    with open(config_file, 'w') as configfile:
        parser.write(configfile)


def aws_select_profile():

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
                logging.error("Token expirado: %s", e)
                os.system("clear")
                print("El token de seguridad ha expirado... Introdúcelo de nuevo...")
                time.sleep(2)
                os.system("clear")
                aws_mfa()

            else:
                print("Error al asumir el role...")
                logging.error("Error al asumir el role: %s", e)

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


def main():

    check_version.check()

    list = [
        "AWS Configure",
        "Select AWS account",
        "MFA token",
        "Select AWS profile",
        "Utilidades",
        "Exit"
    ]

    # Mostrar el menú
    menu = TerminalMenu(menu_entries=list)

    while True:

        clear_screen()
        select = menu.show()

        if select == 0:
            list_credentials_menu = TerminalMenu(
                menu_entries=[
                    "Add AWS credentials",
                    "Add AWS profiles",
                    "List AWS credentials",
                    "List AWS profiles"
                ],
                clear_screen=True
            )
            sub_select = list_credentials_menu.show()
            if sub_select == 0:
                aws_add_credentials()
                pass
            elif sub_select == 1:
                aws_add_profiles()
                pass
            elif sub_select == 2:
                aws_list_credentials()
                pass
            elif sub_select == 3:
                aws_list_profiles()
                pass
        elif select == 1:
            aws_select_credentials()
        elif select == 2:
            aws_mfa()
        elif select == 3:
            aws_select_profile()
        elif select == 4:
            list_credentials_menu = TerminalMenu(
                menu_entries=[
                    "Login ECR"
                ],
                clear_screen=True
            )
            sub_select = list_credentials_menu.show()
            if sub_select == 0:
                login_ecr.check_docker()
                pass
        elif select == 5:
            exit()
    clear_screen()


# Salida con ctrl+c controlada
def sigint_handler(signal, frame):
    clear_screen()
    sys.exit(0)


# Con señal de interrupción, llamada a sigint_handler
signal.signal(signal.SIGINT, sigint_handler)


if __name__ == "__main__":
    main()
