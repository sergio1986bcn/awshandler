import logging
from settings import log_file

# Config de logging
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S'
)

# Obteniene el nombre del módulo actual
logger = logging.getLogger()

# Evita que los mensajes del logger se propaguen a la raíz.
logger.propagate = False
