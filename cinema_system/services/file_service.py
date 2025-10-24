import json
import xml.etree.ElementTree as ET
from typing import Dict, Any, List

from cinema_system.models.booking import Booking
from cinema_system.models.cinema_hall import CinemaHall
from cinema_system.models.exceptions import FileOperationError
from cinema_system.models.film import Film
from cinema_system.models.session import Session
from cinema_system.models.user import User


class JSONFileService:
    """Сохранить данные в JSON файл"""

    @staticmethod
    def save_to_json(data: Dict[str, Any], filename: str) -> None:

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise FileOperationError(f"Ошибка сохранения JSON: {str(e)}")

    """Загрузить данные из JSON файла"""

    @staticmethod
    def load_from_json(filename: str) -> Dict[str, Any]:

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            raise FileOperationError(f"Ошибка загрузки JSON: {str(e)}")


"""Сервис для работы с XML файлами"""


class XMLFileService:
    """Сохранить данные в XML файл"""

    @staticmethod
    def save_to_xml(data: Dict[str, Any], filename: str) -> None:
        try:
            root = ET.Element('cinema_theater')

            # Пользователи
            users_elem = ET.SubElement(root, 'users')
            for user in data.get('users', []):
                user_elem = ET.SubElement(users_elem, 'user')
                ET.SubElement(user_elem, 'id').text = str(user['user_id'])
                ET.SubElement(user_elem, 'name').text = user['name']

            # Залы
            halls_elem = ET.SubElement(root, 'halls')
            for hall in data.get('halls', []):
                hall_elem = ET.SubElement(halls_elem, 'hall')
                ET.SubElement(hall_elem, 'id').text = str(hall['id'])
                ET.SubElement(hall_elem, 'name').text = hall['name']
                ET.SubElement(hall_elem, 'rows').text = str(hall['rows'])
                ET.SubElement(hall_elem, 'seats_per_row').text = str(hall['seats_per_row'])

            # Фильмы
            films_elem = ET.SubElement(root, 'films')
            for film in data.get('films', []):
                film_elem = ET.SubElement(films_elem, 'film')
                ET.SubElement(film_elem, 'id').text = str(film['film_id'])
                ET.SubElement(film_elem, 'title').text = film['title']
                ET.SubElement(film_elem, 'duration').text = str(film['duration'])
                ET.SubElement(film_elem, 'genre').text = film['genre']
                ET.SubElement(film_elem, 'rating').text = str(film['rating'])

            tree = ET.ElementTree(root)
            tree.write(filename, encoding='utf-8', xml_declaration=True)

        except Exception as e:
            raise FileOperationError(f"Ошибка сохранения XML: {str(e)}")




"""Сериализатор данных кинотеатра"""


class DataSerializer:
    """Сериализация в словарь"""
    @staticmethod
    def serialize_cinema_data(cinema_theater) -> Dict[str, Any]:
        return {
            'users': [user.to_dict() for user in cinema_theater.users],
            'halls': [hall.to_dict() for hall in cinema_theater.halls],
            'films': [film.to_dict() for film in cinema_theater.films],
            'sessions': [session.to_dict() for session in cinema_theater.sessions],
            'bookings': [booking.to_dict() for booking in cinema_theater.bookings],
            'next_user_id': cinema_theater.next_user_id,
            'next_booking_id': cinema_theater.booking_service.next_booking_id
        }

    """Десериализация из словаря"""

    @staticmethod
    def deserialize_cinema_data(data: Dict[str, Any]) -> Dict[str, Any]:

        halls = [CinemaHall.from_dict(hall_data) for hall_data in data.get('halls', [])]
        films = [Film.from_dict(film_data) for film_data in data.get('films', [])]
        users = [User.from_dict(user_data) for user_data in data.get('users', [])]

        sessions = []
        for session_data in data.get('sessions', []):
            try:
                session = Session.from_dict(session_data, films, halls)
                sessions.append(session)
            except ValueError as e:
                print(f"Предупреждение: {e}")

        bookings = []
        for booking_data in data.get('bookings', []):
            try:
                booking = Booking.from_dict(booking_data, users, sessions)
                bookings.append(booking)
            except ValueError as e:
                print(f"Предупреждение: {e}")

        return {
            'halls': halls,
            'films': films,
            'users': users,
            'sessions': sessions,
            'bookings': bookings,
            'next_user_id': data.get('next_user_id', 1),
            'next_booking_id': data.get('next_booking_id', 1)
        }
