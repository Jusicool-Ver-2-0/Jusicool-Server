from rest_framework import status
from rest_framework.exceptions import APIException


class UserAlreadyExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User already exist"
    default_code = "user_already_exist"


class CodeIsNotValidException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Code is not valid"
    default_code = "code_is_not_valid"


class UserIsNotValidException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "User is not valid"
    default_code = "user_is_not_valid"
