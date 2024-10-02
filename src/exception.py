# , exc_info() returns the tuple (type(e), e, e.__traceback__). That is, a tuple containing the type of the exception (a subclass of BaseException), the exception itself, and a traceback object which typically encapsulates the call stack at the point where the exception last occurred.

import sys
import logging

def error_message_detail(error,error_detail):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    line_no=exc_tb.tb_lineno
    error_message=f"Error occured in python script {file_name} at line number {line_no} and the error message is {str(error)}"

    return error_message


class customException(Exception):
    def __init__(self,error_message,error_detail):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail)
    
    def __str__(self):
        return self.error_message

