import os
import logging


class Logger:

    def __init__(self, log_file, prefix):

        # Create the log folder if it doesn't exist
        log_folder = os.path.dirname(log_file)
        if not os.path.exists(log_folder):
            os.makedirs(log_folder)

        logger_name = 'logger_'+prefix
        handler_name = 'handler_'+prefix

        # Configure the Shopping Cart logger
        self.logger_name = logging.getLogger(logger_name)
        self.logger_name.setLevel(logging.DEBUG)

        handler_name = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler_name.setFormatter(formatter)
        self.logger_name.addHandler(handler_name)

    def log_message(self, data=None):
        if data is not None:
            # Process the data parameter
            self.logger_name.debug('API call successful: Result is %s', data)
            self.logger_name.info('API call successful: Result is %s', data)
        else:
            self.logger_name.debug(f'API call successful')
            self.logger_name.info(f'API call successful')

    def log_error(self, data):
        self.logger_name.error('An error occurred: %s', data)
