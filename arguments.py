import argparse
from check_version import version

def parse_args():
    parser = argparse.ArgumentParser(description='Descripción de tu aplicación.')
    parser.add_argument('-v', '--version', action='version', version=version,
                        help='Muestra la versión del programa y sale.')
    return parser.parse_args()
    input("Presiona Enter para continuar...")
