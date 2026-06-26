# This script is for exception handling.
import sys
from mlops.logger import logging

logger = logging.getLogger(__name__)

def error_message_detail(error, error_detail:sys):
    # exc_tb contains the error in which line in which file
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno
    error_message = f"""Error occurred in python script name [{file_name}] line number [{line_number}] 
                        error_message {str(error)}"""
    return error_message

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error=error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message
    
# try:
#     1 / 0
# except Exception as e:
#     logger.exception("Division failed")
#     raise CustomException(e, sys)

