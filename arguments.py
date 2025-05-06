import argparse
from check_version import version

def parse_args():
    parser = argparse.ArgumentParser(description='Listado argumentos disponibles.')
    parser.add_argument('-v', '--version', action='version', version=version,
                        help='Muestra la versión del programa y sale.')
    parser.add_argument('-r', '--repo', action='version', version=version,
                        help='Crea un nuevo repositorio. Ejemplo: --repo bitbucket nombre-repositorio')
    return parser.parse_args()
    input("Presiona Enter para continuar...")
