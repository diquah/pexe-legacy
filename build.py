import os
import zlib
import json
import shutil
import base64
import re


def build(target, args):
    MAIN = None
    FILES = list()
    DIR = None

    if target.endswith('.py'):
        MAIN = target.split('\\')[-1]
        FILES = os.listdir('\\'.join(target.split('\\')[0:-1]))
        DIR = '\\'.join(target.split('\\')[0:-1])
    else:
        try:
            FILES = os.listdir(target)
            MAIN = FILES[FILES.index('main.py')]
            DIR = target
        except ValueError:
            print("'main.py' could not be found.")
            return None

    if args['include']:
        new_files = []
        for include in args['include'][0]:
            try:
                valid = re.compile(include)
                for file in FILES:
                    if valid.fullmatch(file) and file not in new_files:
                        new_files.append(file)
            except re.error:
                if include in FILES and include not in new_files:
                    new_files.append(include)
        FILES = new_files
    else:
        new_files = []
        for file in FILES:
            if not file.endswith('.pexe'):
                new_files.append(file)
        FILES = new_files

    if MAIN not in FILES:
        print('Main file is not in list of files. Check your includes.')
        return None

    DATA = {}
    DATA['main'] = MAIN
    DATA['files'] = {}
    DATA['libs'] = {}

    for file in FILES:
        file_dir = DIR + '\\' + file
        if os.path.isfile(file_dir):
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
