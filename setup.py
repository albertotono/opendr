"""
Copyright (C) 2013
Author(s): Matthew Loper

See LICENCE.txt for licensing and contact information.
"""

from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize

from os.path import exists, join
import numpy
import platform
import re

import contexts.autogen



def setup_drender(args):
    setup(name='drender',
            version='0.5',
            packages = ['drender', 'drender.contexts', 'drender.test_dr'],
            package_dir = {'drender': '.'},
            author = 'Matthew Loper',
            author_email = 'matt.loper@gmail.com',
            url = 'http://files.is.tue.mpg/mloper/drender/',
            ext_package='drender',
            package_data={'drender': ['test_dr/nasa*']},
            **args
          )


def add_mesa_args(args):
    libraries = ['OSMesa', 'GL', 'GLU']
    if platform.system()=='Darwin':
        libraries.append('talloc')
    ctx_mesa_extension = Extension("contexts.ctx_mesa", ['contexts/ctx_mesa.c'],
                        language="c",
                        library_dirs=['contexts/OSMesa/lib'],
                        depends=['contexts/_constants.py'],
                        define_macros = [('__OSMESA__', 1)],
                        libraries=libraries)

    args['ext_modules'].append(ctx_mesa_extension)
    args['include_dirs'] += ['.', numpy.get_include(), 'contexts/OSMesa/include']

def add_mac_args(args):
    ctx_mac_extension = Extension("contexts.ctx_mac", ['contexts/ctx_mac.c', 'contexts/ctx_mac_internal.c'],
        language="c",
        depends=['contexts/_constants.py', 'contexts/ctx_mac_internal.h'],
        extra_compile_args=['-framework', 'OpenGL'],
        extra_link_args=['-framework', 'OpenGL'])


    args['ext_modules'].append(ctx_mac_extension)
    args['include_dirs'] += ['.', numpy.get_include()]


def main():
    # Get osmesa and some processed files ready
    contexts.autogen.main()

    # Get context extensions ready
    setup_args = {'ext_modules': [], 'include_dirs': []}
    add_mesa_args(setup_args)
    if platform.system() == 'Darwin':
        add_mac_args(setup_args)

    #setup_args['ext_modules'] = cythonize(setup_args['ext_modules'])

    # Build
    setup_drender(setup_args)


if __name__ == '__main__':
    main()
