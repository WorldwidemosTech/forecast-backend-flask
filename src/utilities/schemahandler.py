import json
import os

from jsonschema import validate, ValidationError

from src.utilities.singleton import Singleton
from src.utilities.exceptions.exceptionfactory import ExceptionFactory


class SchemaHandler(metaclass=Singleton):

    def __init__(self):
        self.user = self._load_schemas('./schemas/')["user"]
        self.property_data = self._load_schemas('./schemas/')["property_data"]
        self.property_info = self._load_schemas('./schemas/')["property_information"]

    @staticmethod
    def _load_schemas(folder: str):
        this_dir = os.path.dirname(__file__)
        directory = os.path.join(this_dir, folder)

        schemas = {}
        for filename in os.listdir(directory):
            if filename.endswith(".json"):
                file_path = os.path.join(directory, filename)
                with open(file_path) as schema_file:
                    schema = json.loads(schema_file.read())
                    schemas[schema['title']] = schema
        return schemas

    def validate_request_body(self, request_body, schema):
        try:
            validate(request_body, schema)
        except ValidationError as error:
            value = request_body
            field_name = None
            for field in error.relative_path:
                value = value[field]
                field_name = field
            if str(error.validator) == "required":
                for key in error.validator_value:
                    if not key in request_body:
                        raise ExceptionFactory(self).invalid_dict_parameter_value(field=key,
                                                                                  failed_field_value=key,
                                                                                  message='Missing value for')

            if str(error.validator) == "enum":
                raise ExceptionFactory(self).invalid_dict_parameter_value(field=field_name, failed_field_value=value)

            if str(error.validator) == 'not' and 'required' in error.validator_value:
                invalid_fields: str = ', '.join(error.validator_value.get('required'))
                raise ExceptionFactory(self).invalid_dict_parameter_value(field=field_name,
                                                                          failed_field_value=invalid_fields,
                                                                          message='The following properties are '
                                                                                  'invalid and should not be present '
                                                                                  f'in {field_name} - ')
            if str(error.validator) == 'maxItems':
                raise ExceptionFactory(self).limit_exceeded(field=field_name, failed_field_value=value)
            if field_name:
                raise ExceptionFactory(self).invalid_dict_parameter_value(field=field_name, failed_field_value=value)
            else:
                raise ExceptionFactory(self).invalid_dict_parameter_value(field=error.message, failed_field_value=value)
        return True

    def validate_user(self, request_body: dict):
        return self.validate_request_body(request_body, self.user)

    def validate_property_data(self, request_body: dict):
        return self.validate_request_body(request_body, self.property_data)
    
    def validate_property_info(self, request_body: dict):
        return self.validate_request_body(request_body, self.property_info)
