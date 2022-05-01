import os
import sys
import zlib
import json
import tempfile
import shutil
import base64
import pathlib


def run(target, args):
    target_dir = (pathlib.Path(target).parent.absolute())

    with open(target, 'rb') as f:
        raw_data = f.read()

    DATA = json.loads(zlib.decompress(raw_data))

    with tempfile.TemporaryDirectory() as temp_dir:
        for name, content in DATA['files'].items():
            with open(temp_dir + '\\' + name, 'w') as f:
                f.write(base64.b64decode(content).decode())
        for name, content in DATA['folders'].items():
            with open(temp_dir + '\\temp.tar', 'wb') as f:
                f.write(base64.b64decode(content))
            shutil.unpack_archive(filename=temp_dir + '\\temp.tar', extract_dir=temp_dir + '\\' + name, format='tar')
            os.remove(temp_dir + '\\temp.tar')

        for file in os.listdir(str(target_dir)):
            if file.endswith('.pll'):
                with open(str(target_dir) + '\\' + file, 'rb') as lib:
                    lib_data = json.loads(zlib.decompress(lib.read()))
                    for name, content in lib_data['files'].items():
                        with open(temp_dir + '\\' + name, 'w') as f:
                            f.write(base64.b64decode(content).decode())
                    for name, content in lib_data['folders'].items():
                        with open(temp_dir + '\\temp.tar', 'wb') as f:
                            f.write(base64.b64decode(content))
                        shutil.unpack_archive(filename=temp_dir + '\\temp.tar', extract_dir=temp_dir + '\\' + name,
                                              format='tar')
                        os.remove(temp_dir + '\\temp.tar')


        with open(temp_dir + '\\' + DATA['main'], 'r') as f:
            new_path = []
            for p in sys.path:
                if not p.lower().find('pexe'):
                    new_path.append(p)
            sys.path = new_path

            sys.argv = [item for sublist in args['args'] for item in sublist]

            exec(f.read())
