import os
import sys
import zlib
import json
import tempfile
import shutil
import base64


def run(target):
    with open(target, 'rb') as f:
        raw_data = f.read()

    DATA = json.loads(zlib.decompress(raw_data))

    with tempfile.TemporaryDirectory() as temp_dir:
        for name, content in DATA['files'].items():
            with open(temp_dir + '\\' + name, 'w') as f:
                f.write(base64.b64decode(content).decode())
        for name, content in DATA['libs'].items():
            with open(temp_dir + '\\temp.tar', 'wb') as f:
                f.write(base64.b64decode(content))
            shutil.unpack_archive(filename=temp_dir + '\\temp.tar', extract_dir=temp_dir + '\\' + name, format='tar')
            os.remove(temp_dir + '\\temp.tar')


        with open(temp_dir + '\\' + DATA['main'], 'r') as f:
            sys.path.append(temp_dir)
            exec(f.read())
