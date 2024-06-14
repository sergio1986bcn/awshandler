# AWSHandler

AWSHandler es un script en Python para la gestión de servicios y recursos de AWS.

## Características

- Configuración de credenciales AWS.
- Selección de cuentas AWS.
- Autenticación MFA.
- Selección de perfiles AWS.
- Autenticación Docker contra ECR.

## Creación entorno virtual python

python3 -m venv awshandler_env
source awshandler_env/bin/activate


## Creación alias

Se tiene que modificar el archivo de configuración de la shell (.bashrc,.zshrc,...) y añadir la siguiente línea:

alias handler='[ruta del proyecto]/main.py'

Después, se tiene que aplicar la nueva configuración con el siguiente comando desde la terminal:

source  ~/.zshrc

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un problema para discutir lo que te gustaría añadir.

## Licencia

[MIT](https://choosealicense.com/licenses/mit/)
