from cinema_system.models import CinemaHall, Film, Session, UserNotFound, SessionNotFoundError, InvalidSeatError, \
    SeatBookedError, BookingError
from cinema_system.services import CinemaTheater, JSONFileService, DataSerializer, XMLFileService


class CinemaApp:

    def __init__(self):
        self.cinema = CinemaTheater()
        self.current_user = None
        self.data_file = "cinema_data.json"
        self._load_data()

    def _load_data(self):
        try:
            data = JSONFileService.load_from_json(self.data_file)
            restored_data = DataSerializer.deserialize_cinema_data(data)

            self.cinema.halls = restored_data['halls']
            self.cinema.films = restored_data['films']
            self.cinema.users = restored_data['users']
            self.cinema.sessions = restored_data['sessions']
            self.cinema.bookings = restored_data['bookings']
            self.cinema.next_user_id = restored_data['next_user_id']
            self.cinema.booking_service.next_booking_id = restored_data['next_booking_id']

            print("Данные успешно загружены!")

        except FileNotFoundError:
            print("Файл данных не найден, создаем новый...")
            self._initialize_sample_data()
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            print("Создаем новые данные...")
            self._initialize_sample_data()

    def _save_data(self):
        try:
            data = DataSerializer.serialize_cinema_data(self.cinema)
            JSONFileService.save_to_json(data, self.data_file)
            XMLFileService.save_to_xml(data, "cinema_data.xml")
            print("Данные успешно сохранены!")
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

    def _initialize_sample_data(self):
        try:
            hall1 = CinemaHall(1, "Красный зал", 5, 8)
            hall2 = CinemaHall(2, "Синий зал", 6, 10)
            self.cinema.add_hall(hall1)
            self.cinema.add_hall(hall2)

            film1 = Film(1, "Человек-Паук", 124, "фантастика", 7.9)
            film2 = Film(2, "Мстители", 187, "фантастика", 8.1)
            film3 = Film(3, "Маша и медведь", 78, "мультфильм", 9.3)
            self.cinema.add_film(film1)
            self.cinema.add_film(film2)
            self.cinema.add_film(film3)

            session1 = Session(1, film1, hall1, "2024-01-20 18:00", 350)
            session2 = Session(2, film2, hall2, "2024-01-21 20:00", 400)
            session3 = Session(3, film3, hall1, "2024-01-22 16:00", 300)
            self.cinema.add_session(session1)
            self.cinema.add_session(session2)
            self.cinema.add_session(session3)

            self._save_data()

        except Exception as e:
            print(f"Ошибка инициализации данных: {e}")

    def run(self):
        print("Добро пожаловать в онлайн-кинотеатр!")

        try:
            while True:
                if not self.current_user:
                    self._show_main_menu()
                else:
                    self._show_user_menu()
        except KeyboardInterrupt:
            print("\n\nСохранение данных...")
            self._save_data()
            print("Выход из программы...")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            self._save_data()

    def _show_main_menu(self):
        print("\n" + "=" * 40)
        print("Онлайн-кинотеатр")
        print("=" * 40)
        print("1. Регистрация")
        print("2. Просмотр фильмов")
        print("3. Поиск сеансов")
        print("4. Сохранить данные")
        print("5. Выход")

        try:
            choice = input("Выберите действие: ").strip()

            if choice == "1":
                self._register_user()
            elif choice == "2":
                self._show_films()
            elif choice == "3":
                self._find_sessions()
            elif choice == "4":
                self._save_data()
            elif choice == "5":
                self._save_data()
                print("До свидания!")
                exit()
            else:
                print("Неверный выбор!")
        except Exception as e:
            print(f"Ошибка в меню: {e}")

    def _show_user_menu(self):
        print(f"\nДобро пожаловать, {self.current_user.name}!")
        print("=" * 40)
        print("1. Просмотр фильмов")
        print("2. Поиск сеансов")
        print("3. Бронирование билета")
        print("4. Мои бронирования")
        print("5. Отмена бронирования")
        print("6. Сохранить данные")
        print("7. Выйти из аккаунта")

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
                self._save_data()
            elif choice == "7":
                self.current_user = None
            else:
                print("Неверный выбор!")
        except Exception as e:
            print(f"Ошибка в меню: {e}")

    def _register_user(self):
        print("\n--- Регистрация ---")
        name = input("Введите ваше имя: ").strip()

        if not name:
            print("Имя не может быть пустым!")
            return

        try:
            user = self.cinema.register_user(name)
            self.current_user = user
            self._save_data()
            print(f"Успешная регистрация! Добро пожаловать, {name}!")
        except Exception as e:
            print(f"Ошибка регистрации: {e}")

    def _show_films(self):
        print("\n--- Все фильмы ---")
        films = self.cinema.films

        if not films:
            print("Фильмы не найдены")
            return

        for i, film in enumerate(films, 1):
            print(f"{i}. {film.title} ({film.genre}) - {film.get_duration_film()} - ★{film.rating}")

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

        except Exception as e:
            print(f"Ошибка поиска: {e}")

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
            self._save_data()
            print(f"Билет успешно забронирован! Номер брони: {booking.booking_id}")

        except (ValueError, IndexError) as e:
            print(f"Неверный ввод: {e}")
        except (UserNotFound, SessionNotFoundError, InvalidSeatError, SeatBookedError, BookingError) as e:
            print(f"Ошибка бронирования: {e}")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

    def _show_my_bookings(self):
        if not self.current_user:
            print("Сначала войдите в систему!")
            return

        print("\n--- Мои бронирования ---")
        bookings = self.current_user.bookings

        if not bookings:
            print("У вас нет активных бронирований")
            return

        for i, booking in enumerate(bookings, 1):
            print(f"{i}. {booking}")

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
                print("Неверный выбор брони!!!")
                return

            selected_booking = bookings[booking_choice]

            success = self.cinema.booking_service.cancel_booking(
                self.current_user.user_id,
                selected_booking.booking_id
            )

            if success:
                self._save_data()
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