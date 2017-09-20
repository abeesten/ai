"""EECS 485 project 1 static site generator."""

from setuptools import setup

setup(
    name='insta485generator',
    version='0.1.0',
    packages=['insta485generator'],
    include_package_data=True,
    install_requires=[
        "click==6.7",
        "jinja2==2.9.6",
        "sh==1.12.14",
    ],
    entry_points={
        'console_scripts': [
            'insta485generator = insta485generator.__main__:main'
        ]
    },
)
