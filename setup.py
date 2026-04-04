from setuptools import find_packages, setup


with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    author='Brian Curnow',
    author_email='bcurnow@users.noreply.github.com',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Natural Language :: English',
    ],
    description='A Connexion-based REST API and database for managing RFID media and permissions.',
    install_requires=[
        'connexion[swagger-ui,uvicorn]>=3.3.0,<4',
        'click>=8.1.0,<9',
    ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='rfidsecuritysvc',
    packages=find_packages(include=['rfidsecuritysvc', 'rfidsecuritysvc.*']),
    package_data={'rfidsecuritysvc.api': ['api.yaml'], 'rfidsecuritysvc.db': ['schema.sql']},
    entry_points={
        'console_scripts': [
            'rfidsecuritysvc-genkey=rfidsecuritysvc.bin.genkey:main',
        ],
    },
    python_requires='>=3.9',
    url='https://github.com/bcurnow/rfid-security-svc',
    version='2.0.0',
)
