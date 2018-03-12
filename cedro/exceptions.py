class HttpAuthenticationError(Exception):
    '''
    Exception to be raised when can not login at Cedro API.
    '''


class ResponseConnectionError(Exception):
    '''
    Exception to be raised when response from Cedro API is not ok.
    '''


class ImprorpelyCalledError(Exception):
    '''
    Exception to be raised when client get called improrpely.
    '''
