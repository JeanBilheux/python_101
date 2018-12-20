import logging

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

def test_me():
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')



if __name__ == "__main__":
    test_me()

## output is
# WARNING:root:This is a warning message
# ERROR:root:This is an error message
# CRITICAL:root:This is a critical message
# WARNING:root:This is a warning message
# ERROR:root:This is an error message
# CRITICAL:root:This is a critical message


## wondering what is this "root" in the message

# Only warning, error and critical are displayed
# because by default, logging logs only message of
# severity WARNING or higher.
# It's possible to change that by changing the configuration of the logging module.

