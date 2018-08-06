# Full tutorial can be found here
# https://tutorialedge.net/python/concurrency/python-processpoolexecutor-tutorial/

from concurrent.futures import ProcessPoolExecutor
import os
import time


def task():
    time.sleep(2)
    print("Executing our task on process # {}".format(os.getpid()))

def main():
    executor = ProcessPoolExecutor(max_workers=3)

    # program does not wait for the first task to be done before moving to the next one

    task1 = executor.submit(task)
    task2 = executor.submit(task)


if __name__ == "__main__":
    main()