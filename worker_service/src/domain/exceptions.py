class DomainException(Exception):
    """Базовое исключение для доменной логики."""
    @property
    def message(self) -> str:
        return "Произошла неизвестная ошибка"


class Forbidden(DomainException):
    @property
    def message(self) -> str:
        return "Недостаточно прав для выполнения операции"
