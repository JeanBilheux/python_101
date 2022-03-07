import logging
import os

THIS_PATH = os.path.abspath(os.path.dirname(__file__))
LOG_FILE = os.path.join(THIS_PATH, "log_of_function2.log")


# def function2():
#     logging.info("Inside function2")
#
# if __name__ == "__main__":
#     logging.basicConfig(filename=LOG_FILE,
#                         filemode='w',
#                         format="[%(levelname)s] - %(asctime)s - %(message)s",
#                         level=logging.INFO)
#
#     print("here")
#     logging.info("*** Logging anything happening in function2.py ***")
#
#     function2()

# logging.basicConfig(filename=LOG_FILE,
#                     filemode='w',
#                     format="[%(levelname)s] - %(asctime)s - %(message)s",
#                     level=logging.INFO)
#
# print("here")
# logging.info("*** Logging anything happening in function2.py ***")

# shimin way
logging.basicConfig(filename=LOG_FILE,
                    filemode='w',
                    format='%(asctime)s %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger.info("*** logging anything happening in function2.py ***")
