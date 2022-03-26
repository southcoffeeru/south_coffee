import json
import os


def init():
    global CONFIG
    with open(os.environ.get('CONFIG_PATH', 'config.json')) as config:
        CONFIG = json.load(config)
