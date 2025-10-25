from cinema_system.models.cinema_hall import CinemaHall
from cinema_system.models.film import Film
from cinema_system.models.session import Session
from cinema_system.services.cinema_service import CinemaTheater
from models.exceptions import *


class CinemaApp:
    def __init__(self):
        self.cinema = CinemaTheater()
        self.current_user = None
        self._initialize_sample_data()

    """Инициализация тестовыми данными"""
    def _initialize_sample_data(self):
        try:
            hall1 = CinemaHall(1, "Красный зал", 5, 8)
            hall2 = CinemaHall(2, "Синий зал", 6, 10)
            self.cinema.add_hall(hall1)
            self.cinema.add_hall(hall2)

            film1 = Film(1, "Человек-паук", 162, "фантастика", 8.1)
            film2 = Film(2, "Остров проклятых", 169, "фантастика", 8.6)
            film3 = Film(3, "Маша и медведь", 88, "мультфильм", 8.5)
            self.cinema.add_film(film1)
            self.cinema.add_film(film2)
            self.cinema.add_film(film3)

            session1 = Session(1, film1, hall1, "18:00", 350)
            session2 = Session(2, film2, hall2, "20:00", 560)
            session3 = Session(3, film3, hall1, "16:00", 700)
            self.cinema.add_session(session1)
            self.cinema.add_session(session2)
            self.cinema.add_session(session3)

        except Exception as e:
            print(f"Ошибка инициализации данных: {e}")

    """Запуск"""
    def run(self):

        print("Добро пожаловать в онлайн-кинотеатр!")

        while True:
            try:
                if not self.current_user:
                    self._show_main_menu()
                else:
                    self._show_user_menu()
            except KeyboardInterrupt:
                print("\n\nВыход из программы...")
                break
            except Exception as e:
                print(f"Неожиданная ошибка: {e}")

    """Главное меню"""
    def _show_main_menu(self):
        print("\n" + "=" * 40)
        print("Онлайн-кинотеатр")
        print("=" * 40)
        print("1. Регистрация")
        print("2. Просмотр фильмов")
        print("3. Поиск сеансов")
        print("4. Выход")

        try:
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._register_user()
            elif choice == "2":
                self._show_films()
            elif choice == "3":
                self._find_sessions()
            elif choice == "4":
                print("До свидания!")
                exit()
            else:
                print("Неверный выбор!")
        except Exception as e:
            print(f"Ошибка в меню: {e}")

    """Меню пользователя"""
    def _show_user_menu(self):
        print(f"\nДобро пожаловать, {self.current_user.name}!")
        print("=" * 40)
        print("1. Просмотр фильмов")
        print("2. Поиск сеансов")
        print("3. Бронирование билета")
        print("4. Мои бронирования")
        print("5. Отмена бронирования")
        print("6. Выйти из аккаунта")

        try:
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._show_films()
            elif choice == "2":
                self._find_sessions()
            elif choice == "3":
                self._book_ticket()
            elif choice == "4":
                self._show_my_bookings()
            elif choice == "5":
                self._cancel_booking()
            elif choice == "6":
                self.current_user = None
            else:
                print("Неверный выбор!")
        except Exception as e:
            print(f"Ошибка в меню: {e}")

    """Регистрация пользователя"""
    def _register_user(self):
        print("\n--- Регистрация ---")
        name = input("Введите ваше имя: ").strip()

        if not name:
            print("Имя не может быть пустым!")
            return

        try:
            user = self.cinema.register_user(name)
            self.current_user = user
            print(f"Успешная регистрация! Добро пожаловать, {name}!")
        except ValueError as e:
            print(f"Ошибка регистрации: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    """Показать все фильмы"""
    def _show_films(self):
        print("\n--- Все фильмы ---")
        films = self.cinema.films

        if not films:
            print("Фильмы не найдены")
            return

        for i, film in enumerate(films, 1):
            print(f"{i}. {film.title} ({film.genre}) - {film.get_duration_film()} - ★{film.rating}")

    """Поиск сеансов по названию фильма"""
    def _find_sessions(self):
        print("\n--- Поиск сеансов ---")
        movie_title = input("Введите название фильма: ").strip()

        if not movie_title:
            print("Название фильма не может быть пустым!")
            return

        try:
            sessions = self.cinema.find_sessions_by_movie(movie_title)

            if not sessions:
                print(f"Сеансы для фильма '{movie_title}' не найдены")
                return

            print(f"\nНайдено сеансов: {len(sessions)}")
            for i, session in enumerate(sessions, 1):
                available_seats = len(session.hall.get_available_seats())
                print(f"{i}. {session.movie.title}")
                print(f"   Зал: {session.hall.name}, Время: {session.time}")
                print(f"   Свободных мест: {available_seats}, Цена: {session.price} руб.")

        except ValueError as e:
            print(f"Ошибка поиска: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    """Бронирование билета"""
    def _book_ticket(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return

        print("\n--- Бронирование билета ---")

        try:
            movie_title = input("Введите название фильма: ").strip()
            sessions = self.cinema.find_sessions_by_movie(movie_title)

            if not sessions:
                print(f"Сеансы для фильма '{movie_title}' не найдены")
                return

            print("\nДоступные сеансы:")
            for i, session in enumerate(sessions, 1):
                available_seats = len(session.hall.get_available_seats())
                print(f"{i}. {session.time} - Зал: {session.hall.name} - {available_seats} мест")

            session_choice = int(input("Выберите сеанс: ")) - 1

            if session_choice < 0 or session_choice >= len(sessions):
                print("Неверный выбор сеанса!")
                return

            selected_session = sessions[session_choice]

            available_seats = selected_session.hall.get_available_seats()

            if not available_seats:
                print("Нет доступных мест на этот сеанс!")
                return

            print(f"\nДоступные места:")

            seats_by_row = {}
            for row, seat in available_seats:
                if row not in seats_by_row:
                    seats_by_row[row] = []
                seats_by_row[row].append(seat)

            for row in sorted(seats_by_row.keys()):
                print(f"Ряд {row}: {', '.join(map(str, sorted(seats_by_row[row])))}")

            row = int(input("Введите номер ряда: "))
            seat = int(input("Введите номер места: "))

            booking = self.cinema.booking_service.create_booking(
                self.current_user.user_id,
                selected_session.session_id,
                row,
                seat
            )
            print(f"Билет успешно забронирован! Номер брони: {booking.booking_id}")

        except (ValueError, IndexError) as e:
            print(f"Неверный ввод: {e}")
        except (UserNotFound, SessionNotFoundError, InvalidSeatError, SeatBookedError, BookingError) as e:
            print(f"Ошибка бронирования: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


    """Показать бронирования пользователя"""
    def _show_my_bookings(self):

        if not self.current_user:
            print("Сначала войдите в систему")
            return

        print("\n--- Мои бронирования ---")
        bookings = self.current_user.bookings

        if not bookings:
            print("У вас нет активных бронирований")
            return

        for i, booking in enumerate(bookings, 1):
            print(f"{i}. {booking}")

    """Отмена бронирования"""
    def _cancel_booking(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return

        print("\n--- Отмена бронирования ---")
        bookings = self.current_user.bookings

        if not bookings:
            print("У вас нет активных бронирований")
            return

        try:
            for i, booking in enumerate(bookings, 1):
                print(f"{i}. {booking}")

            booking_choice = int(input("Выберите бронь для отмены: ")) - 1

            if booking_choice < 0 or booking_choice >= len(bookings):
                print("Неверный выбор брони!")
                return

            selected_booking = bookings[booking_choice]

            success = self.cinema.booking_service.cancel_booking(
                self.current_user.user_id,
                selected_booking.booking_id
            )

            if success:
                print("Бронь успешно отменена!")
            else:
                print("Ошибка отмены брони")

        except (ValueError, IndexError) as e:
            print(f"Неверный ввод: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")


if __name__ == "__main__":
    app = CinemaApp()
    app.run()