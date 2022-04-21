from src.utilities.exceptions.exception import APIException, Error


class ExceptionFactory:

    def __init__(self, invoker):
        # Store the name of the class, whether we received a class
        # or an instance of it
        if type(invoker) == type:
            self.inv_class = invoker.__module__
        elif type(invoker) == str:
            self.inv_class = invoker
        else:
            self.inv_class = type(invoker).__module__

    def not_authorized(self) -> APIException:
        return APIException(
            self.inv_class,
            http_code=401,
            error=Error.NOT_AUTHORIZED,
            description="Not Authorized",
        )

    def internal_server_error(self, internal_message: str, description: str = 'Internal server error') \
            -> APIException:
        return APIException(
            self.inv_class,
            http_code=500,
            error=Error.INTERNAL_SERVER_ERROR,
            description=description,
            internal_message=internal_message
        )

    def resource_not_found(
            self,
            internal_message: str = "Resource not found", field: str = None, failed_field_value: str = None,
            http_code: int = 404) \
            -> APIException:
        return APIException(
            self.inv_class,
            http_code=http_code,
            error=Error.RESOURCE_NOT_FOUND,
            description=internal_message if field is None
            else "{} : the {} is incorrect".format(internal_message, field),
            field=field,
            failed_field_value=[failed_field_value]
        )

    def incorrect_request_body(self, internal_message: str = None) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.INCORRECT_REQUEST_BODY,
            description="Invalid request body",
            internal_message=internal_message
        )

    def invalid_parameter_value(self, param_name: str) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.INVALID_PARAMETER_VALUE,
            description=param_name,
        )

    def invalid_dict_parameter_value(self, field: str = None, failed_field_value: str = None,
                                     message: str = 'Invalid value for') -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.INVALID_DICT_PARAMETER_VALUE,
            description=f'{message} {failed_field_value}',
            field=field,
            failed_field_value=failed_field_value
        )

    def invalid_header_value(self, header_name: str) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.INVALID_HEADER_VALUE,
            description=header_name,
        )

    def duplicate_resource(self) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.DUPLICATE_RESOURCE,
            description="Duplicate resource not allowed",
            internal_message="Multiple objects matched in DB"
        )

    def invalid_auth_type(self) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.INVALID_AUTH_TYPE,
            description="Invalid connection type",
        )

    def invalid_credentials(self, internal_message: str = None) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.INVALID_CREDENTIALS,
            description="Credentials are invalid",
            internal_message=internal_message
        )

    def invalid_auth0_token(self):
        return APIException(
            self.inv_class,
            http_code=500,
            error=Error.INVALID_AUTH0_TOKEN,
            description="Internal Server Error",
            internal_message="Received an invalid Auth0 token",
        )

    def not_permitted(self) -> APIException:
        return APIException(
            self.inv_class,
            http_code=403,
            error=Error.NOT_PERMITTED,
            description="Not Permitted",
        )

    def api_service_error(self, internal_message: str, http_code: int = 400, retry: bool = False) -> APIException:
        return APIException(
            self.inv_class,
            http_code=http_code,
            error=Error.API_SERVICE_ERROR,
            description="Internal Server Error",
            internal_message=internal_message,
            retry=retry
        )

    def api_version_not_supported(self, internal_message: str = None) -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.API_VERSION_NOT_SUPPORTED,
            description="This API version is not supported for this request",
            internal_message=internal_message
        )

    def limit_exceeded(self, field: str = None, failed_field_value: str = None,
                       message: str = 'Limit exceeded for') -> APIException:
        return APIException(
            self.inv_class,
            http_code=400,
            error=Error.LIMIT_EXCEEDED,
            description=f'{message} {failed_field_value}',
            field=field,
            failed_field_value=failed_field_value
        )

    def database_operation_failed(self) -> APIException:
        return APIException(
            self.inv_class,
            http_code=500,
            error=Error.DATABASE_OPERATION_FAIL,
            description="Database operation failed, document not found",
        )
