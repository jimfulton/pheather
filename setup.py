name = 'pheather'
version = '0.1.1.dev0'

install_requires = ['numpy', 'pandas', 'ZODB', 'newt.db', 'feather-format']
extras_require = dict(test=['manuel', 'mock', 'zope.testing'])

entry_points = """
"""

from setuptools import setup

def read(path):
    with open(path) as f:
        return f.read()

long_description = read('README.rst') + '\n\n' + read('CHANGES.rst')

setup(
    author = 'Jim Fulton',
    author_email = 'jim@jimfulton.info',
    license = 'MIT',

    name = name, version = version,
    long_description = long_description,
    description = long_description.strip().split('\n')[1],
    packages = [name],
    url='https://github.com/jimfulton/pheather',
    package_dir = {'': 'src'},
    install_requires = install_requires,
    zip_safe = False,
    entry_points=entry_points,
    package_data = {name: ['*.txt', '*.test', '*.html']},
    extras_require = extras_require,
    tests_require = extras_require['test'],
    test_suite = name+'.tests.test_suite',
    keywords=['persistent', 'pandas', 'data frame', 'zodb', 'persistent',
              'database'],
    )
