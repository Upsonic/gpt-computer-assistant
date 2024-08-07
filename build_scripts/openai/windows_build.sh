#!/bin/sh
# Requireed installations
python -m pip install ".[base]"
python -m pip install '.[agentic]'
python -m pip install pyinstaller==6.9.0


# Pyinstaller
pyinstaller app.spec
