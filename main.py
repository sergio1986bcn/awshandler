#!/usr/bin/python3

from simple_term_menu import TerminalMenu
import signal
import sys
import os

import check_version

# from aws_credentials import (
#     aws_add_credentials,
#     aws_list_credentials,
#     aws_select_credentials,
#     aws_mfa
# )
# from aws_profiles import (
#     aws_add_profiles,
#     aws_list_profiles,
#     aws_select_profile
# )

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():

    check_version.check()

    list = [
        "AWS Configure",
        "Select AWS account",
        "MFA token",
        "Select AWS profile",
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
