import os
import argparse
from .utils.db import set_profile
from .gpt_computer_assistant import QApplication, MainWindow, sys

def start():

    # get --profile argument with library

    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", help="profile to use")
    args = parser.parse_args()
    profile = args.profile
    print("Profile:", profile)

    if profile is not None:  
        set_profile(profile)

    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"

    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
