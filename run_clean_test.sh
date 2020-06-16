#!/bin/bash
pip install -U pip && \
pip freeze | xargs pip uninstall -y && \
python setup.py install && \
pip install -r requirements-dev.txt && \
pytest tests
