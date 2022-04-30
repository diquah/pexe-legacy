import os
import zlib
import json
import shutil
import base64


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
    DATA['libs'] = {}

    for file in FILES:
        file_dir = DIR + '\\' + file
        if os.path.isfile(file_dir):
            if not file.endswith('.pexe'):
                with open(file_dir, 'rb') as f:
                    DATA['files'][file] = base64.b64encode(f.read()).decode()
        elif os.path.isdir(file_dir):
            shutil.make_archive(DIR + '\\temp_archive', 'tar', root_dir=file_dir)
            with open(DIR + '\\temp_archive.tar', 'rb') as f:
                DATA['libs'][file] = base64.b64encode(f.read()).decode()
            os.remove(DIR + '\\temp_archive.tar')

    BUILD_FILE_PATH = DIR + '\\application.pexe'

    with open(BUILD_FILE_PATH, 'wb') as f:
        json_data = json.dumps(DATA)
        f.write(zlib.compress(json_data.encode()))

    return BUILD_FILE_PATH
