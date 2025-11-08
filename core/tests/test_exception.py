import pytest
from rest_framework.exceptions import APIException

from core.exceptions import InternalServerError, NotFoundError


class TestException:
    def test_api_error(self):
        """ApiError 클래스를 테스트합니다.
        해당 클래스가 정확히 APIException을 호출하는지 검증합니다.
        """
        with pytest.raises(APIException) as error:
            raise NotFoundError

        assert error.value.status_code == 404
        assert error.value.error_code == "NOT_FOUND_ERROR"
        assert error.value.message == "요청하신 데이터를 찾을 수 없습니다."
