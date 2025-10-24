from .film import Film
from .cinema_hall import CinemaHall


class Session:
    def __init__(self, session_id: int, movie: Film, hall: CinemaHall,
                 time: str, price: int):
        self.session_id = session_id
        self.movie = movie
        self.hall = hall
        self.time = time
        self.price = price

    def __repr__(self) -> str:
        return (f"Сеанс:\n"
                f"Фильм: {self.movie.title}\n"
                f"Зал: {self.hall.name}\n"
                f"Время: {self.time}\n"
                f"Цена: {self.price} руб.")

    """Сериализация в словарь"""

    def to_dict(self) -> dict:
        return {
            'session_id': self.session_id,
            'movie_id': self.movie.film_id,
            'hall_id': self.hall.id,
            'time': self.time,
            'price': self.price
        }

    @classmethod
    def from_dict(cls, data: dict, films: list, halls: list) -> 'Session':
        movie = next((f for f in films if f.film_id == data['movie_id']), None)
        hall = next((h for h in halls if h.id == data['hall_id']), None)

        if not movie or not hall:
            raise ValueError("Не найден фильм или зал для сеанса")

        return cls(data['session_id'], movie, hall, data['time'], data['price'])