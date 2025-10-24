class Film:
    """Инициализация фильма"""
    def __init__(self, film_id: int, title: str, duration: int, genre: str, rating: float = 0.0):
        self.film_id = film_id
        self.title = title
        self.duration = duration
        self.genre = genre
        self.rating = rating

    """Геттер отформатированной длительности фильма"""
    def get_duration_film(self) -> str:
        hours = self.duration // 60
        minutes = self.duration % 60
        formatted_duration = f"{hours}ч {minutes}мин"
        return formatted_duration

    """Сериализация в словарь"""
    def to_dict(self) -> dict:
        film_dict = {
            'film_id': self.film_id,
            'title': self.title,
            'duration': self.duration,
            'genre': self.genre,
            'rating': self.rating
            }
        return film_dict

    """Десериализация словаря"""
    @classmethod
    def from_dict(cls, data: dict) -> 'Film':
        film = cls(data['film_id'], data['title'], data['duration'], data['genre'], data['rating'])
        return film

    def __repr__(self) -> str:
        return (f"ID фильма: {self.film_id}\n"
                f"Название: {self.title}\n"
                f"Длительность в минутах: {self.duration}\n"
                f"Жанр: {self.genre}\n"
                f"Рейтинг: {self.rating}\n")

