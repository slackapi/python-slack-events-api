#!/bin/bash
pip install -U pip && \
pip freeze | grep -v '-e' | xargs pip uninstall -y && \
pip install MarkupSafe && \
python setup.py install && \
pip install -r requirements-dev.txt && \
pytest tests
