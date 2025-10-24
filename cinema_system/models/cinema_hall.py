from typing import List, Tuple, Union
from .exceptions import InvalidSeatError, SeatBookedError


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

    """Метод для резервирования места в зале"""

    def reserve_seat(self, row: int, seat: int) -> bool:

        if not self.is_valid_seat(row, seat):
            raise InvalidSeatError(f"Указано неверное место: {row} ряд, {seat} место")

        seat_key = (row, seat)
        if seat_key in self.reserved_seats:
            raise SeatBookedError(f"{seat} место, {row} ряд уже забронированы")

        self.reserved_seats.add(seat_key)
        return True

    """Освободить место"""

    def to_free_seat(self, row: int, seat: int) -> bool:

        if not self.is_valid_seat(row, seat):
            raise InvalidSeatError(f"Указано неверное место: {row} ряд, {seat} место")

        seat_key = (row, seat)
        if seat_key not in self.reserved_seats:
            raise SeatBookedError(f"Место и так свободно")

        self.reserved_seats.remove(seat_key)
        return True

    """Геттер доступных для бронирования мест"""

    def get_available_seats(self) -> List[Tuple[int, int]]:
        all_seats = [(r, s) for r in range(1, self.rows + 1)
                     for s in range(1, self.seats_per_row + 1)]
        available_seats = [seat for seat in all_seats if seat not in self.reserved_seats]
        return available_seats

    """Геттер карты зала с забронированными и доступными местами"""

    def get_map_hall(self) -> List[Union[Tuple[int, int], str]]:
        matrix = []
        for row in range(1, self.rows + 1):
            for seat in range(1, self.seats_per_row + 1):
                seat = (row, seat)
                if seat in self.reserved_seats:
                    matrix.append('X')
                else:
                    matrix.append(seat)
        return matrix

    """Сериализация в словарь"""
    def to_dict(self) -> dict:
        hall_dict = {
            "id": self.id,
            "name": self.name,
            "rows": self.rows,
            "seats_per_row": self.seats_per_row,
            "total_seats": self.total_seats,
            "reserved_seats": list(self.reserved_seats)
        }
        return hall_dict

    """Десериализация словаря в объект класса"""
    @classmethod
    def from_dict(cls, data: dict) -> 'CinemaHall':
        hall = cls(data['id'], data['name'], data['rows'], data['seats_per_row'])
        hall.reserved_seats = set(tuple(seat) for seat in data['reserved_seats'])
        hall.total_seats = data['total_seats']
        return hall

    """Спец-метод для более приятного отображения объектов класса"""
    def __repr__(self) -> str:
        return (f"CinemaHall(id={self.id}, name='{self.name}', "
                f"rows={self.rows}, seats_per_row={self.seats_per_row}, "
                f"total_seats={self.total_seats}, "
                f"reserved_seats={len(self.reserved_seats)})")
