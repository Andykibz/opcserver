from setuptools import setup

setup(
    name='s71200opc',
    version='0.1dev',
    packages=['myplc','index','myserver'],
    license='MIT',
    author='Andrew Kibor',
    author_email='andykibz@gmail.com',
    long_description="Connect PLC to opcserver",
    install_requires=[
        'cffi',
        'Click',
        'cryptography',
        'Flask',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'itsdangerous',
        'Jinja2',
        'lxml',
        'MarkupSafe',
        'opcua',
        'pycparser',
        'python-dateutil',
        'python-snap7',
        'pytz',
        'six',
        'SQLAlchemy',
        'Werkzeug',
        'WTForms'
      ],
)
