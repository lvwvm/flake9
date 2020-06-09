# -*- coding: utf-8 -*-
import setuptools

setuptools.setup(
    name='flake9-example-plugin',
    license='MIT',
    version='1.0.0',
    description='Example plugin to Flake9',
    author='Ian Cordasco',
    author_email='graffatcolmingov@gmail.com',
    url='https://gitlab.com/pycqa/flake9',
    package_dir={'': 'src/'},
    packages=['flake9_example_plugin'],
    entry_points={
        'flake9.extension': [
            'X1 = flake9_example_plugin:ExampleOne',
            'X2 = flake9_example_plugin:ExampleTwo',
        ],
    },
    classifiers=[
        'Framework :: Flake9',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
