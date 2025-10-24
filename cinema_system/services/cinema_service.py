from typing import List, Optional

from .booking_service import BookingService
from ..models.booking import Booking
from ..models.cinema_hall import CinemaHall
from ..models.film import Film
from ..models.session import Session
from ..models.user import User


class CinemaTheater:

    def __init__(self):
        self.halls: List[CinemaHall] = []
        self.films: List[Film] = []
        self.sessions: List[Session] = []
        self.users: List[User] = []
        self.bookings: List[Booking] = []
        self.next_user_id = 1
        self.booking_service = BookingService(self)

    """Добавить кинозал"""

    def add_hall(self, hall: CinemaHall) -> None:
        if not isinstance(hall, CinemaHall):
            raise ValueError("Должен быть объект CinemaHall")
        self.halls.append(hall)

    """Найти зал по ID"""

    def get_hall(self, hall_id: int) -> Optional[CinemaHall]:
        if not isinstance(hall_id, int) or hall_id <= 0:
            raise ValueError("ID зала должен быть положительным числом")

        for hall in self.halls:
            if hall.id == hall_id:
                return hall
        return None

    """Добавить фильм"""

    def add_film(self, film: Film) -> None:
        if not isinstance(film, Film):
            raise ValueError("Должен быть объект Film")
        self.films.append(film)

    """Найти фильм по ID"""

    def get_film(self, film_id: int) -> Optional[Film]:
        if not isinstance(film_id, int) or film_id <= 0:
            raise ValueError("ID фильма должен быть положительным числом")

        for film in self.films:
            if film.film_id == film_id:
                return film
        return None

    """Найти фильмы по названию"""

    def find_films_by_title(self, title: str) -> List[Film]:
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Название фильма не может быть пустым")

        films = []
        for film in self.films:
            if title.lower() in film.title.lower():
                films.append(film)
        return films

    """Добавить сеанс"""

    def add_session(self, session: Session) -> None:
        if not isinstance(session, Session):
            raise ValueError("Должен быть объект Session")
        self.sessions.append(session)

    """Найти сеанс по ID"""

    def get_session(self, session_id: int) -> Optional[Session]:
        if not isinstance(session_id, int) or session_id <= 0:
            raise ValueError("ID сеанса должен быть положительным числом")

        for session in self.sessions:
            if session.session_id == session_id:
                return session
        return None

    """Найти сеансы по названию фильма"""

    def find_sessions_by_movie(self, movie_title: str) -> List[Session]:
        if not isinstance(movie_title, str) or not movie_title.strip():
            raise ValueError("Название фильма не может быть пустым")

        sessions = []
        for session in self.sessions:
            if movie_title.lower() in session.movie.title.lower():
                sessions.append(session)
        return sessions

    """Зарегистрировать пользователя"""

    def register_user(self, name: str) -> User:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")

        user = User(self.next_user_id, name)
        self.users.append(user)
        self.next_user_id += 1
        return user

    """Найти пользователя по ID"""

    def get_user(self, user_id: int) -> Optional[User]:
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("ID пользователя должен быть положительным числом")

        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    """Найти пользователя по имени"""

    def find_user_by_name(self, name: str) -> Optional[User]:
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")

        for user in self.users:
            if name.lower() in user.name.lower():
                return user
        return None

    def __repr__(self) -> str:
        return (f"Кинотеатр:\n"
                f"Залы: {len(self.halls)}\n"
                f"Фильмы: {len(self.films)}\n"
                f"Сеансы: {len(self.sessions)}\n"
                f"Пользователи: {len(self.users)}\n"
                f"Брони: {len(self.bookings)}")
