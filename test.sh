source venv/bin/activate
pip3 install -r requirements-testing.txt
pytest
mypy ThingiBrowser
