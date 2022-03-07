import logging
import subprocess
import os

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = os.path.join(THIS_PATH, "log_of_main.log")
CMD = "python " + os.path.join(THIS_PATH, "function2.py")


def function1():
    proc = subprocess.Popen(CMD, shell=True, stdin=subprocess.PIPE, universal_newlines=True)
    proc.communicate()


if __name__ == "__main__":
    logging.basicConfig(filename=LOG_FILE,
                        filemode='w',
                        format="[%(levelname)s] - %(asctime)s - %(message)s",
                        level=logging.INFO)

    logging.info("*** Logging anything happening in main.py ***")

    function1()
