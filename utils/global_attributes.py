import os
import json

config = json.load(open("./config.json", 'r', encoding="utf-8"))

def construct_path(*path):
    return "." + os.path.join(*path).replace('\\', '/')