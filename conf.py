from constants import PATH_TO_CONF_FILE
from json import loads

def get_config():
    with open(PATH_TO_CONF_FILE, 'r') as conf_file:
        buff:dict = conf_file.read()
        config:dict = loads(buff)
        config['blacklist']:set[str] = set(config['blacklist'])
        return config
