from typing import List, Tuple, Set
from .exceptions import InvalidSeatError, SeatAlreadyBookedError


class CinemaHall:
    """Инициализация кинозала"""
    def __init__(self, hall_id: int, name: str, rows: int, seats_per_row: int):
        self.id = hall_id
        self.name = name
        self.rows = rows
        self.seats_per_row = seats_per_row
        self.total_seats = seats_per_row * rows
        self.reserved_seats = set()

    """Метод для проверки валидности указанного места в зале"""
    def is_valid_seat(self, row: int, seat: int) -> bool:
        if 0 < row <= self.rows and 0 < seat <= self.seats_per_row:
            return True
        raise InvalidSeatError()

    """Метод для бронирования места"""
    def reserve_seat(self, row: int, seat: int) -> bool:

        if not self.is_valid_seat(row, seat):
            raise InvalidSeatError(f"Указано неверное место: {row} ряд, {seat} место")

        seat_key = (row, seat)
        if seat_key in self.reserved_seats:
            raise SeatAlreadyBookedError(f"{seat} место, {row} ряд уже забронированы")

        self.reserved_seats.add(seat_key)
        return True



