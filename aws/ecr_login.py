# login_ecr.py
import boto3
import base64
import docker
import time


# Verifica si Docker está funcionando y luego loguea contra ECR.
def check_docker():

    try:
        docker_client = docker.from_env()
        docker_client.ping()
        print("El servicio docker está levantado...")
        login(docker_client)
    except docker.errors.DockerException:
        print("El servicio docker no está levantado...")
        time.sleep(2)
        return


# Extrae usuario y contraseña y se valida contra docker
def login(docker_client):
    client = boto3.client('ecr')
    response = client.get_authorization_token()
    user, password = base64.b64decode(
        response['authorizationData'][0]['authorizationToken']
    ).decode().split(':')
    registry = response['authorizationData'][0]['proxyEndpoint']

    try:
        docker_client.login(user, password, registry=registry)
        print("Registro contra Docker correcto...")
        time.sleep(2)
    except docker.errors.APIError:
        print("Error en el registro contra Docker...")
