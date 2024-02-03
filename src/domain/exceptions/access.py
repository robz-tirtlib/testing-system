from src.domain.exceptions.base import DomainError


class AccessDenied(DomainError):
    def __init__(self, msg = None) -> None:
        self._msg = msg
    def __str__(self):
        return self._msg if self._msg else "No access"
