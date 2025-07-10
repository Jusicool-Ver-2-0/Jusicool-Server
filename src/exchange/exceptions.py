from rest_framework import status
from rest_framework.exceptions import APIException


class ShortageUSDBalanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Shortage USD balance"
    default_code = "shortage_usd_balance"


class ShortageKRWBalanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Shortage KRW balance"
    default_code = "shortage_krw_balance"
