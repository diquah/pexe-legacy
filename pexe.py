import logging
import argparse
from build import build
from run import run

PEXE_VERSION = '0.1.0'
logging.basicConfig(format='%(levelname)s: %(message)s')

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--build', action='store_true')
parser.add_argument('-i', '--include', action='append', nargs='*')
parser.add_argument('-l', '--lib', action='append', nargs='*')

parser.add_argument('-r', '--run', action='store_true')
parser.add_argument('-a', '--args', action='append', nargs='*')

parser.add_argument('target')

args = vars(parser.parse_args())
args['version'] = PEXE_VERSION

if not args['run'] and not args['build']:
    args['run'] = True

if args['args'] is None:
    args['args'] = []

target = args['target']
BUILD_FILE_PATH = None

if args['build']:
    BUILD_FILE_PATH = build(target, args)
    if BUILD_FILE_PATH:
        print('BUILD SUCCESSFUL!')
    else:
        quit(100)

if args['run']:
    if args['build']:
        target = BUILD_FILE_PATH
    args['args'].insert(0, [target])

    if target.endswith('.pexe'):
        run(target, args)