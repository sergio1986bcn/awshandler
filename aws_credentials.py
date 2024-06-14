import getpass
import configparser
from settings import aws_credentials_file, aws_config_file, config_file
import re
from simple_term_menu import TerminalMenu

parser = configparser.ConfigParser()


def add():
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


def list():
    with open(aws_credentials_file, 'r') as infile:
        for line in infile:
            res = re.findall(r"\[([\w-]+)\]", line)
            if res:
                print(" ".join(res))
        print('\n')
        input("Pulsa cualquier tecla para volver al menú principal...")


def select():

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
        