#! /usr/bin/python3

import logging

class Logger:
#Logger class constructor
    def __init__(self, file_path):
        self.file_path = file_path
        logging.basicConfig(filename=self.file_path,format='%(asctime)s %(levelname)s | %(message)s', datefmt='[%m/%d/%Y][%H:%M:%S]', level=logging.INFO)
        logging.info('')
        logging.info('_____START_____')

#Function that appends message to the log file
    def append(self,lvl,msg):
        if lvl == 1:
            logging.debug(msg)
        elif lvl == 2:
            logging.info(msg)
        elif lvl == 3:
            logging.warning(msg)
        elif lvl == 4:
            logging.error(msg)

#Logger class destructor
    def __del__(self):
        logging.info('_____STOP_____')
        logging.info('')
