from glob import glob
import re
import time
from os import path, environ
import sys
import shutil
dst_wscom_f = 'wscript_common.py'
if not path.exists('wscript_common.py'):
    wscom_f = environ['DEEP3D_BASE']+'/deep3d/base/wscript_common.py'
    shutil.copy2(wscom_f, '.')

from wscript_common import base_options_C, base_configure_C, bld_shlib

def options(opt):
    base_options_C(opt)

def configure(conf):
    base_configure_C(conf)
    env = conf.env
    if sys.platform == 'win32':
        conf.env.append_value('DEFINES', ['__thread=__declspec(thread)', 'WIN32',  'MSC',  '_CRT_SECURE_NO_DEPRECATE', 'USE_GKREGEX', '_WINDLL'])

def extract_version(base_d):
    for l in open(base_d+'/include/metis.h'):
        parts = l.split()
        if len(parts) < 3:
            continue
        if parts[1] == 'METIS_VER_MAJOR':
            v0 = parts[-1]
        elif parts[1] == 'METIS_VER_MINOR':
            v1 = parts[-1]
        elif parts[1] == 'METIS_VER_SUBMINOR':
            v2 = parts[-1]
            return v0+'.'+v1+'.'+v2
    raise

def build(bld):
    env = bld.env
    ver = extract_version('.')

    mod = 'metis'
    bld_shlib(bld, source=glob('libmetis/*.c')+glob('GKlib/*.c'), target=mod, use=['m'], includes=['include', 'GKlib', 'libmetis'], vnum=ver)
