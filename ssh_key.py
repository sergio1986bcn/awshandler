import subprocess
import os

def generate ():

    key_name = input('Introduce el nombre de la clave SSH (sin extensión): ')
    email = input('Introduce el correo electrónico: ')
    key_path = input('Introduce directorio donde guardar la clave (Presiona Enter para usar ~/.ssh): ') or '~/.ssh'

    # Expande la ruta para sustituir la virgulilla
    key_path = os.path.expanduser(key_path)

    # Crea el directorio si no existe
    if not os.path.exists(key_path):
        os.makedirs(key_path)

    # Ruta completa del archivo de la clave
    full_key_path = os.path.join(key_path, key_name)

    # Verificar si ya existe una clave con el mismo nombre
    if os.path.exists(full_key_path) or os.path.exists(f"{full_key_path}.pub"):
        print(f'Ya existe una llave SSH con el nombre {key_name} en {key_path}.')
        return None

    # Comando para generar la clave SSH
    command = ['ssh-keygen', '-t', 'ed25519', '-b', '4096','-C', email, '-f', full_key_path, '-N', '']

    try:
        subprocess.run(command, check=True)
        print(f'Llave SSH generada en {full_key_path}')
        return full_key_path
    except subprocess.CalledProcessError as e:
        print(f'Error al generar la llave SSH: {e}')
        return None