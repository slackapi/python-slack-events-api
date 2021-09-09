#!/bin/bash

script_dir=`dirname $0`
cd ${script_dir}/..
rm -rf ./slackeventsapi.egg-info

pip install -U pip && \
  pip install twine wheel && \
  rm -rf dist/ build/ slackeventsapi.egg-info/ && \
  python setup.py sdist bdist_wheel && \
  twine check dist/* && \
  twine upload dist/*
