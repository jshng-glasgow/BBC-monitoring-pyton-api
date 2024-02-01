#!/usr/bin/env python
"""error_handling.py : A collection of errors to raise for the API"""
__author__ = "Joseph Shingleton"

class URLNotFoundError(Exception):
    """Exception raised for urls which cannot be found.
    Attributes:
        url : Input url which caused the errror.
        message : Explanation of the error.
    """
    
    def __init__(self, url, message=False):
        self.url = url
        if message:
            self.message = message
        else:
            self.message = f'{url} can not be found'
        super().__init__(self.message)
        
        
class AuthorizationError(Exception):
    """Exception raised login attempts with incorrect credentials.
    Attributes:
        username : Input username which caused the errror.
        masked_password : Masked password which caused the error.
        message : Explanation of the error.
    
    Hidden attributed
        
    """
    def __init__(self, credentials):
        # get username and password from credentials
        self.username = credentials.get('username')
        self.__password = credentials.get('password')
        # mask the password
        self.masked_password = '*'*len(self.__password) 
        self.message = f'Unsuccessful authorization for username: {self.username} and password: {self.masked_password}'
        super().__init__(self.message)
        
        
class InternalServerError(Exception):
    """Exception for when BBC Monitoring has server connection issues
    Attributes:
        message : Explanation of error
    """
    def __init__(self):
        self.message = "BBC Monitoring can not currently be acccessed."
        super().__init__(self.message)
        
        
class SubscriptionError(Exception):
    """Exception to handel requests for content which are not available under 
    the users current subscription
    Attributes:
        message : Explanation of the error.
    """
    def __init__(self):
        self.message = ("The requested content is not available under your current subscription.")
        super().__init__(self.message)


class TsAndCsError(Exception):
    """Exception to handle attempts to log in using an account which as not
    yet accepted the terms and conditions
    attributes:
        message : Explanation of the error.
    """
    def __init__(self):
        self.message = ("BBC Monitoring Terms and Conditions not yet accepted.")
        super().__init__(self.message)
    
    
class LimitExceededError(Exception):
    """Exception to handle request limit being exceeded.
    attributes:
        message : Explanation of the error.
    """
    def __init__(self):
        self.message = ("The rate limit of 60 requests per second has been exceeded")
        super().__init__(self.message)