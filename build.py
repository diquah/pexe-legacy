import os
import zlib
import json

def build(target):
    MAIN = None
    FILES = list()
    DIR = None

    if target.endswith('.py'):
        MAIN = target.split('\\')[-1]
        FILES = os.listdir('\\'.join(target.split('\\')[0:-1]))
        DIR = '\\'.join(target.split('\\')[0:-1])
    else:
        FILES = os.listdir(target)
        MAIN = FILES[FILES.index('main.py')]
        DIR = target

    DATA = {}
    DATA['main'] = MAIN
    DATA['files'] = {}

    for file in FILES:
        if file.endswith('.py'):
            with open(DIR + '\\' + file, 'r') as f:
                DATA['files'][file] = f.read()

    BUILD_FILE_PATH = DIR + '\\application.pexe'

    with open(BUILD_FILE_PATH, 'wb') as f:
        json_data = json.dumps(DATA)
        f.write(zlib.compress(json_data.encode()))

    return BUILD_FILE_PATH