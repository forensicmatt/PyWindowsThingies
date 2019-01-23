from winthingies import __version__
from setuptools import setup

setup(
    name='winthingies',
    version=__version__,
    description='Tools and Lib doing cool Windows things.',
    author='Matthew Seyer',
    url='https://github.com/forensicmatt/PyWindowsThingies',
    license='Apache License (2.0)',
    packages=[
        'winthingies',
        'winthingies.win32'
    ],
    install_requires=[
		'pywin32',
        'ujson'
    ],
    scripts=[
        'scripts/print_handles.py'
    ]
)