#!/usr/bin/python3

import aws
from core import check_version, settings
import utils
import arguments
from utils.repositories.actions.github_actions import crear_repositorio_github

from simple_term_menu import TerminalMenu
import signal
import sys
import os

def clear_screen():
    os.system('clear')

def main():

    check_version.check()

    # Argumentos del comando
    args = arguments.parse_args()

    menu_entries = [
        "AWS Configure",
        "Select AWS account",
        "MFA token",
        "Select AWS profile",
        "Utilidades",
        "Exit"
    ]
    
    sub_menu_entries = {
        "AWS Configure": [
            "Add AWS credentials",
            "Add AWS profiles",
            "List AWS credentials",
            "List AWS profiles"
        ],
        "Utilidades": [
            "Login ECR",
            "Create SSH key",
            "Create repositories"
        ],
        "Repositorios": [
            "GitHub",
            "Bitbucket"
        ]
    }
    
    sub_actions = {
        "AWS Configure": {
            0: aws.credentials.add,
            1: aws.profiles.add,
            2: aws.credentials.list,
            3: aws.profiles.list
        },
        "Utilidades": {
            0: aws.ecr_login.check_docker,
            1: utils.ssh_key.generate,
            2: lambda: handle_sub_menu(sub_menu_entries["Repositorios"], "Repositorios")
        },
        "Repositorios": {
            0: crear_repositorio_github,
            1: lambda: print("Bitbucket: Funcionalidad no implementada aún.")
        }
    }

    main_actions = {
        0: lambda: handle_sub_menu(sub_menu_entries["AWS Configure"], "AWS Configure"),
        1: aws.credentials.select,
        2: aws.mfa.check,
        3: aws.profiles.select,
        4: lambda: handle_sub_menu(sub_menu_entries["Utilidades"], "Utilidades"),
        5: sys.exit
    }
    
    def handle_sub_menu(sub_menu_list, parent_menu=None):
        sub_menu = TerminalMenu(menu_entries=sub_menu_list, clear_screen=True)
        sub_select = sub_menu.show()

        if sub_select is None:
            return
        
        if parent_menu:
            action = sub_actions.get(parent_menu, {}).get(sub_select)
            if action:
                action()
        else:
            action = main_actions.get(sub_select)
            if action:
                action()
    
    menu = TerminalMenu(menu_entries=menu_entries)

    while True:
        clear_screen()
        select = menu.show()
        if select is None:
            break
        action = main_actions.get(select)
        if action:
            action()
        else:
            print("Opción inválida en menú principal")


# Salida con ctrl+c controlada
def sigint_handler(signal, frame):
    clear_screen()
    sys.exit(0)

# Con señal de interrupción, llamada a sigint_handler
signal.signal(signal.SIGINT, sigint_handler)


if __name__ == "__main__":
    main()
