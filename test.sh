#!/usr/bin/env bash
set -eo pipefail
python3 -m py.test --cov=ThingiBrowser --cov-fail-under=10
