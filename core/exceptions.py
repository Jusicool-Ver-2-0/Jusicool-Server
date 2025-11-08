from rest_framework import status
from rest_framework.exceptions import APIException


class ApiError(APIException):
    status_code: int
    error_code: str
    message: str

    def __init__(self):
        super().__init__(detail=self.message, code=self.error_code)


class NotFoundError(ApiError):
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "NOT_FOUND_ERROR"
    message = "요청하신 데이터를 찾을 수 없습니다."


class InternalServerError(ApiError):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "INTERNAL_SERVER_ERROR"
    message = "내부 서버에 에러가 발생했습니다. 관리자에게 문의하세요."
