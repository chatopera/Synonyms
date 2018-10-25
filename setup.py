# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
LONGDOC = """
Synonyms
=====================

Chinese Synonyms for Natural Language Processing and Understanding.

Welcome
-------

"""

setup(
    name='synonyms',
    version='3.10.0',
    description='Chinese Synonyms for Natural Language Processing and Understanding',
    long_description=LONGDOC,
    author='Hai Liang Wang, Hu Ying Xi',
    author_email='hailiang.hl.wang@gmail.com',
    url='https://github.com/huyingxi/Synonyms',
    license="MIT",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic'],
    keywords='corpus,machine-learning,NLU,NLP,Synonyms,Similarity',
    packages=find_packages(),
    install_requires=[
        'six>=1.11.0',
        'numpy>=1.13.1',
        'scipy==1.0.0',
        'scikit-learn==0.19.1',
        'absl-py==0.1.10'
    ],
    package_data={
        'synonyms': [
            '**/*.gz',
            '**/*.txt',
            '**/*.vector',
            'LICENSE']})
