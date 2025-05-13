from core.settings import aws_credentials_file, config_file
from core.logger import logger

from simple_term_menu import TerminalMenu
import configparser
import boto3
import botocore.exceptions
import time
import os

parser = configparser.ConfigParser()


def check():
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
    elif len(arn_mfa) == 1:
        arn_mfa = arn_mfa[0]['SerialNumber']
    else:
        print("No hay dispositivos MFA asociados al usuario...")
        time.sleep(2)
        return

    # Guardo el mfa seleccionado en el archivo de configuración
    parser.clear()
    parser.read(config_file)
    parser.set('general', 'mfa', arn_mfa)
    with open(config_file, 'w') as configfile:
        parser.write(configfile)

    while True:
        mfa = input("Ingrese el código MFA: ")
        if len(mfa) != 6:
            logger.error("El código MFA ingresado no tiene 6 dígitos --- %s", mfa)
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
                    logger.error("Error en el código MFA ingresado: %s", e)
                    os.system("clear")
                    print("Has introducido mal el MFA, inténtalo de nuevo.")
                    time.sleep(2)
                    os.system("clear")
                else:
                    print("Error al obtener las credenciales MFA")
                    logger.error("Error al obtener las credenciales MFA: %s", e)

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
