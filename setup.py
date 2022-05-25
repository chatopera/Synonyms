# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
LONGDOC = """
Synonyms
=====================

中文近义词

https://github.com/chatopera/Synonyms

"""

setup(
    name='synonyms',
    version='3.18.0',
    description='中文近义词：聊天机器人，智能问答工具包；Chinese Synonyms for Natural Language Processing and Understanding',
    long_description=LONGDOC,
    author='Hai Liang Wang, Hu Ying Xi',
    author_email='hain@chatopera.com',
    url='https://github.com/chatopera/Synonyms',
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
        'Programming Language :: Python :: 3.7',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Indexing',
        'Topic :: Text Processing :: Linguistic'],
    keywords='corpus,machine-learning,NLU,NLP,Synonyms,Similarity,chatbot',
    packages=find_packages(),
    install_requires=[
        'six>=1.11.0',
        'numpy>=1.13.1',
        'scipy>=1.0.0',
        'scikit-learn>=0.19.1',
        'jieba>=0.40'
    ],
    package_data={
        'synonyms': [
            '**/**/idf.txt',
            '**/**/*.p',
            '**/*.gz',
            '**/*.txt',
            'LICENSE']})
