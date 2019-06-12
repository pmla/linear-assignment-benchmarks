import os
import sys
import numpy
from distutils.core import setup, Extension

major_version = 0
minor_version = 1

python_version = "%d.%d%s" % (sys.version_info.major,
                              sys.version_info.minor,
                              sys.abiflags)

module1 = Extension('jonkervolgenant',
                    define_macros = [('MAJOR_VERSION', str(major_version)),
                                     ('MINOR_VERSION', str(minor_version))],
                    include_dirs = [os.path.join(numpy.get_include(), 'numpy')],
                    libraries = [],
                    library_dirs = [],
                    extra_compile_args = ["-std=c++11"],
                    extra_link_args = ["-lm", "-lpython%s" % (python_version)],
                    sources = ['jonkervolgenant_module.c',
                               'jonkervolgenant.cpp',
])

setup(name = 'rectangular',
       version = '%d.%d' % (minor_version, minor_version),
       description = 'Jonker-Volgenant module',
       author = 'P. M. Larsen',
       author_email = 'pmla@mit.edu',
       url = 'https://github.com/pmla/linear-assignment-benchmarks',
       long_description = '''
Development module for rectangular assignment problem''',
       ext_modules = [module1])
