class CinemaError(Exception):
    """Базовое исключение для кинотеатров"""
    pass


class SeatAlreadyBookedError(CinemaError):
    """Исключение, место забронировано"""
    pass


class InvalidSeatError(CinemaError):
    """Неверный номер места"""
    pass


class SessionNotFoundError(CinemaError):
    """Сеанс не найден"""
    pass


class FileOperationError(CinemaError):
    """Ошибка работы с файлами"""
    pass

