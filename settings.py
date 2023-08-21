import os

# Ruta donde se encuentra el script
dir_path = os.path.dirname(os.path.realpath(__file__))

# Ruta del archivo de log
log_file = os.path.join(dir_path, 'error.log')

# Ruta del archivo de configuración
config_file = os.path.join(dir_path, 'config.ini')
