#! /bin/bash 
###########################################
#
###########################################

# constants
baseDir=$(cd `dirname "$0"`;pwd)
export PYTHONUNBUFFERED=1
export PATH=/opt/miniconda3/envs/venv-py3/bin:$PATH

# functions

# main 
[ -z "${BASH_SOURCE[0]}" -o "${BASH_SOURCE[0]}" = "$0" ] || return
cd $baseDir/..

if [ ! -d tmp ]; then
    mkdir tmp
fi

if [ -f synonyms/data/words.vector.gz ]; then
    echo "Move pkg to tmp"
    mv synonyms/data/words.vector.gz tmp
fi

rm -rf ./dist/*
python setup.py sdist
twine upload --skip-existing dist/*

if [ -f tmp/words.vector.gz ]; then
    mv tmp/words.vector.gz synonyms/data/words.vector.gz
fi

