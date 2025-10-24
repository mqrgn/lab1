class CinemaError(Exception):
    """Базовое исключение для кинотеатров"""
    pass


class SeatBookedError(CinemaError):
    """Место забронировано"""
    """Или место и так свободно"""
    pass


class InvalidSeatError(CinemaError):
    """Неверный номер места"""
    pass


class SessionNotFoundError(CinemaError):
    """Сеанс не найден"""
    pass


class UserNotFound(CinemaError):
    """Пользователь не найден"""
    pass


class BookingError(CinemaError):
    """Ошибка бронирования"""
    pass


class FileOperationError(CinemaError):
    """Ошибка работы с файлами"""
    pass
