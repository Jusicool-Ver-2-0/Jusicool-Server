from rest_framework import status
from rest_framework.exceptions import APIException


class AccountAlreadyExistException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Account already exist'
    default_code = 'account_already_exist'


class CodeIsNotValidException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Code is not valid'
    default_code = 'code_is_not_valid'