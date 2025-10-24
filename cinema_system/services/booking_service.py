from cinema_system.models.booking import Booking
from cinema_system.models.exceptions import *


class BookingService:
    def __init__(self, cinema_theater):
        self.cinema = cinema_theater
        self.next_booking_id = 1

    """Создать бронирование билета"""
    def create_booking(self, user_id: int, session_id: int, row: int, seat: int) -> Booking:

        try:
            user = self.cinema.get_user(user_id)
            session = self.cinema.get_session(session_id)

            if not user:
                raise UserNotFound(f"Пользователь с ID {user_id} не найден")
            if not session:
                raise SessionNotFoundError(f"Сеанс с ID {session_id} не найден")

            hall = session.hall

            if not hall.is_valid_seat(row, seat):
                raise InvalidSeatError(f"Неверное место: ряд {row}, место {seat}")

            hall.reserve_seat(row, seat)

            booking = Booking(self.next_booking_id, user, session, row, seat)
            self.next_booking_id += 1

            self.cinema.bookings.append(booking)
            user.add_booking(booking)

            return booking

        except Exception as e:
            if session:
                session.hall.free_seat(row, seat)
            raise BookingError(f"Ошибка бронирования: {str(e)}")

    """Отменить бронирование"""
    def cancel_booking(self, user_id: int, booking_id: int) -> bool:
        user = self.cinema.get_user(user_id)
        if not user:
            return False

        for booking in user.bookings:
            if booking.booking_id == booking_id:
                booking.session.hall.free_seat(booking.row, booking.seat)
                user.bookings.remove(booking)
                self.cinema.bookings.remove(booking)
                return True

        return False

    def __repr__(self) -> str:
        return f"Сервис бронирования: всего броней - {len(self.cinema.bookings)}"