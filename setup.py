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
          'Flask',
          'opcua',
          'python-snap7',
          'SQLAlchemy',
          'Flask-SQLAlchemy',
          'cryptography',
          'WTForms',
          'Flask-WTF'
      ],
)
