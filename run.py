import sys
import zlib
import json
import tempfile
from pprint import pp

def run(target):
    with open(target, 'rb') as f:
        raw_data = f.read()

    DATA = json.loads(zlib.decompress(raw_data))

    with tempfile.TemporaryDirectory() as temp_dir:
        for name, content in DATA['files'].items():
            with open(temp_dir + '\\' + name, 'w') as f:
                f.write(content)

        with open(temp_dir + '\\' + DATA['main'], 'r') as f:
            sys.path.append(temp_dir)
            exec(f.read())
