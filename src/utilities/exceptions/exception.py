from enum import IntEnum


class Error(IntEnum):
    NOT_AUTHORIZED = 1
    INTERNAL_SERVER_ERROR = 2
    RESOURCE_NOT_FOUND = 3
    DUPLICATE_RESOURCE = 4
    INCORRECT_REQUEST_BODY = 5
    INVALID_PARAMETER_VALUE = 6
    INVALID_HEADER_VALUE = 7
    HTTP_REQUEST_ERROR = 8
    INVALID_AUTH_TYPE = 9
    INVALID_CREDENTIALS = 10
    INVALID_AUTH0_TOKEN = 11
    NOT_PERMITTED = 12
    API_SERVICE_ERROR = 13
    INVALID_DICT_PARAMETER_VALUE = 14
    API_VERSION_NOT_SUPPORTED = 15
    LIMIT_EXCEEDED = 16
    DATABASE_OPERATION_FAIL = 17


class APIException(Exception):
    """Anything that goes wrong in the API Service"""

    def __init__(self, inv_class,
                 http_code: int, error: Error, description: str,
                 internal_message: str = "", field: str = None, failed_field_value: list = None,
                 retry: bool = False):
        """
           Args:
               inv_class: The class that invoked the exception.
               http_code: The HTTP code that should be returned to the
                          API user about this exception.
               error: Data Integration Error Code.
               description: Will also be returned to the API user.
                            However, will likely not be displayed. The UX
                            will have their own message for the DI Code.
               internal_message: The internal error message to be logged.
               field: The field that caused exception.
               failed_field_value: The value that caused exception.
               retry: Should the failing action be retried.
        """
        self.inv_class = inv_class
        self.http_code = http_code
        self.error = error
        self.description = description
        self.internal_message = internal_message
        self.field = field
        self.failed_field_value = failed_field_value
        self.retry = retry
        super().__init__(description)
