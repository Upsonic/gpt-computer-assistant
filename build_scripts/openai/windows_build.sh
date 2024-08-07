#!/bin/sh


# Pyinstaller
pip3 install '.[base]'
pip3 install '.[agentic]'
pyinstaller --recursive-copy-metadata gpt_computer_assistant run.py --windowed --add-data="gpt_computer_assistant/utils/media/*":"gpt_computer_assistant/utils/media" --icon="gpt_computer_assistant/utils/media/icon.ico" --name="GPT Computer Assistant"
