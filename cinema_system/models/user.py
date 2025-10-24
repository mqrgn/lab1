class User:

    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.bookings = []

    """Добавить бронирование пользователю"""
    def add_booking(self, booking) -> None:
        self.bookings.append(booking)

    def __repr__(self) -> str:
        return (f"Пользователь:\n"
                f"ID: {self.user_id}\n"
                f"Имя: {self.name}\n"
                f"Броней: {len(self.bookings)}")

    """Сериализация в словарь"""

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'name': self.name
        }

    """Десериализация из словаря"""

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(data['user_id'], data['name'])