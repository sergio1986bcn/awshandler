from pathlib import Path

# Rutas definidas
dir_path = Path(__file__).parent.parent
home = str(Path.home())

# Ruta del archivo de log
log_file = dir_path / 'error.log'

# Ruta del archivo de configuración
config_file = dir_path / 'config.ini'

# Rutas config aws cli
aws_credentials_file = home + "/.aws/credentials"
aws_config_file = home + "/.aws/config"