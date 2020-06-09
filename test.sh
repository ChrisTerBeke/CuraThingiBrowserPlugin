#!/usr/bin/env bash
set -e
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
pyenv activate cura
pip3 install -r requirements-testing.txt
pytest
mypy ThingiBrowser
pyenv deactivate
