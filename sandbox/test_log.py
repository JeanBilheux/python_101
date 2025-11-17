import logging

LOG_FILE_NAME = "my_log.log"
logging.basicConfig(filename=LOG_FILE_NAME,
                            filemode='w', 
                            format="[%(levelname)s] - %(asctime)s - %(message)s",
                            level=logging.INFO)
        
logging.info(f"*** Starting AiAutomatedLoop - version 03/06/2025")

logging.info("*** Starting checking for new files - version 03/06/2025")
print(f"check log file at {LOG_FILE_NAME}")