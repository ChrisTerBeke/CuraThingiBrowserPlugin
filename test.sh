#!/usr/bin/env bash
set -e
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
export PYENV_VIRTUALENV_DISABLE_PROMPT=1
pyenv activate cura
pytest
mypy ThingiBrowser
pyenv deactivate
