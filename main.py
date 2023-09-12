#!/usr/bin/python3

import aws_credentials
import aws_profiles
import aws_mfa
import check_version
import login_ecr


from simple_term_menu import TerminalMenu
import signal
import sys
import os


def clear_screen():
    os.system('clear')


def main():

    check_version.check()

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
            "Login ECR"
        ]
    }
    
    main_actions = {
        0: lambda: handle_sub_menu(sub_menu_entries["AWS Configure"]),
        1: aws_credentials.select,
        2: aws_mfa.check,
        3: aws_profiles.select,
        4: lambda: handle_sub_menu(sub_menu_entries["Utilidades"]),
        5: sys.exit
    }
    
    sub_actions = {
        "AWS Configure": {
            0: aws_credentials.add,
            1: aws_profiles.add,
            2: aws_credentials.list,
            3: aws_profiles.list
        },
        "Utilidades": {
            0: login_ecr.check_docker
        }
    }
    
    def handle_sub_menu(sub_menu_list):
        sub_menu = TerminalMenu(menu_entries=sub_menu_list, clear_screen=True)
        sub_select = sub_menu.show()
        parent_menu = menu_entries[select]
        sub_actions[parent_menu][sub_select]()
    
    menu = TerminalMenu(menu_entries=menu_entries)

    while True:
        clear_screen()
        select = menu.show()
        main_actions[select]()


# Salida con ctrl+c controlada
def sigint_handler(signal, frame):
    clear_screen()
    sys.exit(0)

# Con señal de interrupción, llamada a sigint_handler
signal.signal(signal.SIGINT, sigint_handler)


if __name__ == "__main__":
    main()
