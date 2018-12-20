import logging

def try_me():
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

if __name__ == "__main__":

    logging.basicConfig(filename='/Users/j35/Desktop/app.cfg',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')
    logging.warning("This should go to a file")

    try_me()
