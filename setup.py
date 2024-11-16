from setuptools import setup, find_packages

setup(
    name='tarjan_planner',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'networkx',
        'geopy',
        'matplotlib'
    ],
    entry_points={
        'console_scripts': [
            'tarjan_planner=tarjan_planner.main:main',
        ],
    },
    package_data={
        '': ['data/*.json'],
    },
    include_package_data=True,
)