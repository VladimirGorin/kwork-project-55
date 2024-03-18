import configparser

config = configparser.ConfigParser()
config.read("./assets/config.ini")

def get(section, key):
    return config[section][key]
