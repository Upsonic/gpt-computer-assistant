# create an function to check system is windows
def is_windows():
    import platform
    return platform.system() == 'Windows'

# check if system is windows
if is_windows():
    # if system is windows, then start the application
    # fix start
    import sys
    import os

    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w")
    # fix end



from gpt_computer_assistant import start






start()







