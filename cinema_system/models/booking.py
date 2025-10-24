from datetime import datetime
from .user import User
from .session import Session


class Booking:
    """Инициализация брони"""

    def __init__(self, booking_id: int, user: User, session: Session, row: int, seat: int):
        self.booking_id = booking_id
        self.user = user
        self.session = session
        self.row = row
        self.seat = seat

    def __repr__(self):
        return (f"Бронь #{self.booking_id}: {self.session.movie.title}, "
                f"ряд {self.row}, место {self.seat}")

    """Сериализация в словарь"""

    def to_dict(self) -> dict:
        return {
            'booking_id': self.booking_id,
            'user_id': self.user.user_id,
            'session_id': self.session.session_id,
            'row': self.row,
            'seat': self.seat,
        }

    """Десериализация"""

    @classmethod
    def from_dict(cls, data: dict, users: list, sessions: list) -> 'Booking':
        user = next((u for u in users if u.user_id == data['user_id']), None)
        session = next((s for s in sessions if s.session_id == data['session_id']), None)

        if not user or not session:
            raise ValueError("Не найден пользователь или сеанс")

        return cls(data['booking_id'], user, session, data['row'], data['seat'])