#!/bin/sh
# Requireed installations
python -m pip install ".[base]"
python -m pip install '.[agentic]'
python -m pip install pyinstaller==6.9.0


# Pyinstaller
pip3 uninstall pyqt5 -y
pip3 install pyqt5==5.15.10

pip3 uninstall pynput -y
pip3 install pynput==1.7.3

pip3 uninstall langchain-google-genai -y
pip3 install langchain-google-genai==1.0.4

pip3 uninstall langchain-groq -y
pip3 install langchain-groq==0.1.5


pip3 uninstall numpy -y
pip3 install numpy

pyinstaller --recursive-copy-metadata gpt_computer_assistant run.py --windowed --add-data="gpt_computer_assistant/utils/media/*":"gpt_computer_assistant/utils/media" --icon="gpt_computer_assistant/utils/media/icon.ico" --name="GPT Computer Assistant"
