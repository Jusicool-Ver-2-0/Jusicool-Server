from rest_framework import status
from rest_framework.exceptions import APIException


class ShortageKRWBalanceException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Shortage KRW balance'
    default_code = 'shortage_krw_balance'


class InvalidQuantityException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid quantity'
    default_code = 'invalid_quantity'


class TradePriceFetchException(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'Trade price fetch error'
    default_code = 'trade_error'


class NotFountOrderException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Order not found'
    default_code = 'not_found_order'