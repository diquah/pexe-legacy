import os
import zlib
import json
import shutil
import base64
import logging
import re


def build(target, args):
    MAIN = None
    FILES = list()
    LIBS = list()
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
            logging.error("'main.py' could not be found.")
            return None

    if args['include']:
        includes = sum(args['include'], [])
        new_files = []
        for include in includes:
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
            if not file.endswith('.pexe') and file != 'bin':
                new_files.append(file)
        FILES = new_files


    if MAIN not in FILES:
        logging.error('Main file is not in list of files. Check your includes.')
        return None

    if not os.path.exists(DIR + '\\bin'):
        os.mkdir(DIR + '\\bin')

    BUILD_FILE_PATH = DIR + '\\bin'

    DATA = {}
    DATA['version'] = args['version']
    DATA['main'] = MAIN
    DATA['files'] = {}
    DATA['folders'] = {}

    for file in FILES:
        file_dir = DIR + '\\' + file
        if os.path.isfile(file_dir):
            with open(file_dir, 'rb') as f:
                DATA['files'][file] = base64.b64encode(f.read()).decode()
        elif os.path.isdir(file_dir):
            shutil.make_archive(DIR + '\\temp_archive', 'tar', root_dir=file_dir)
            with open(DIR + '\\temp_archive.tar', 'rb') as f:
                DATA['folders'][file] = base64.b64encode(f.read()).decode()
            os.remove(DIR + '\\temp_archive.tar')

    if args['lib']:
        for lib in args['lib']:
            lib_data = {}
            lib_data['version'] = args['version']
            lib_data['files'] = {}
            lib_data['folders'] = {}

            for file in lib:
                file_dir = DIR + '\\' + file
                if os.path.isfile(file_dir):
                    with open(DIR + '\\' + file, 'rb') as f:
                        lib_data['files'][file] = base64.b64encode(f.read()).decode()
                elif os.path.isdir(file_dir):
                    shutil.make_archive(DIR + '\\temp_archive', 'tar', root_dir=file_dir)
                    with open(DIR + '\\temp_archive.tar', 'rb') as f:
                        lib_data['folders'][file] = base64.b64encode(f.read()).decode()
                    os.remove(DIR + '\\temp_archive.tar')

            with open(BUILD_FILE_PATH + '\\' + '&'.join(lib) + '.pll', 'wb') as f:
                json_data = json.dumps(lib_data)
                f.write(zlib.compress(json_data.encode()))

    with open(BUILD_FILE_PATH + '\\application.pexe', 'wb') as f:
        json_data = json.dumps(DATA)
        f.write(zlib.compress(json_data.encode()))

    return BUILD_FILE_PATH + '\\application.pexe'
