import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DOCU_DIR = os.path.join(BASE_DIR, "documents")

LOG_DIR = os.path.join(BASE_DIR, "logs")

CONFIG_DIR = os.path.join(BASE_DIR, "config")

to_be_built_folder = [LOG_DIR, DOCU_DIR, ]
USER_CONFIG_JSON_DIR = os.path.join(CONFIG_DIR, "user_config.json")
GLOBAL_CONFIG_DIR = os.path.join(CONFIG_DIR, "global_config.toml")
for each in to_be_built_folder:
    if not os.path.exists(each):
        os.makedirs(each)
