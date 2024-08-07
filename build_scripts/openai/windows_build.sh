#!/bin/sh
# Requireed installations
python -m pip install ".[base]"
python -m pip install '.[agentic]'
python -m pip install pyinstaller==6.9.0


# Pyinstaller
pip3 uninstall -r requirements.in -y
pip3 install -r requirements.in

pip3 uninstall numpy -y
pip3 install numpy

pyinstaller --recursive-copy-metadata gpt_computer_assistant run.py --windowed --onefile --add-data="gpt_computer_assistant/utils/media/*":"gpt_computer_assistant/utils/media" --icon="gpt_computer_assistant/utils/media/icon.ico" --name="GPT Computer Assistant"
