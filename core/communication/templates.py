"""Base templates for communication."""

from abc import ABC, abstractmethod
from typing import Any


class EmailTemplate(ABC):
    """이메일 템플릿 추상 클래스"""

    @abstractmethod
    def get_subject(self) -> str:
        """이메일 제목 반환"""
        pass

    @abstractmethod
    def get_template_name(self) -> str:
        """템플릿 파일명 반환"""
        pass

    @abstractmethod
    def get_context(self) -> dict[str, Any]:
        """템플릿 컨텍스트 반환"""
        pass

    @property
    def recipient_email(self) -> str:
        """수신자 이메일"""
        raise NotImplementedError("recipient_email must be implemented")
