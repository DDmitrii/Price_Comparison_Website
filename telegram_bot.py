import telebot
from initial_parse import db

# Инициализация бота
BOT_TOKEN = '7828869023:AAHv5nHMayfWrHgBxM2u4uI7G5-hHN6JSK8'
bot = telebot.TeleBot(BOT_TOKEN)

USER_CONTEXT = {}


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Команда /start или /help: Приветствие и описание функционала.
    """
    bot.reply_to(
        message,
        "Привет! Я бот для подбора книг по доступным ценам. Вот что я умею:\n"
        "1. Сравнить цены на книгу по ее названию: /find_book_by_name\n"
        "2. Показать все книги автора: /find_book_by_author\n"
        "3. Подобрать похожие книги: /find_similar_books\n"
        "4. Найти книги по жанру: /find_book_by_genre\n"
        "\nВведите команду, а затем отправьте название книги, автора или жанра."
    )


@bot.message_handler(commands=['find_book_by_name'])
def ask_for_book_name(message):
    """
    Запрашивает у пользователя название книги для команды /find_book_by_name.
    """
    bot.reply_to(message, "Введите название книги (например, 'Гарри Поттер'):")
    bot.register_next_step_handler(message, handle_book_by_name)


def handle_book_by_name(message):
    """
    Вывод книг по возрастанию цены.
    """
    book_name = message.text.strip()
    books = db.get_book_by_name(book_name)
    if books:
        books.sort(key=lambda b: b.price)  # Сортируем по цене
        response = "Книги по возрастанию цены:\n"
        for book in books:
            response += f"{book.name} - {book.price:.2f} руб. (Жанры: {[genre.name for genre in book.genres]})\n"
    else:
        response = "Книг с таким названием не найдено."
    bot.reply_to(message, response)


@bot.message_handler(commands=['find_book_by_author'])
def ask_for_author_name(message):
    """
    Запрашивает у пользователя имя автора для команды /find_book_by_author.
    """
    bot.reply_to(message, "Введите имя автора (например, 'Джоан Роулинг'):")
    bot.register_next_step_handler(message, handle_author)


def handle_author(message):
    """
    Вывод всех книг указанного автора.
    """
    author_name = message.text.strip()
    books = db.get_books_by_author(author_name)
    if books:
        response = f"Книги автора {author_name}:\n"
        for book in books:
            response += f"{book.name} - {book.price:.2f} руб. (Жанры: {[genre.name for genre in book.genres]})\n"
    else:
        response = f"Книг автора {author_name} не найдено."
    bot.reply_to(message, response)


@bot.message_handler(commands=['find_book_by_genre'])
def ask_for_genre_name(message):
    """
    Запрашивает у пользователя название жанра для команды /find_book_by_genre.
    """
    bot.reply_to(message, "Введите название жанра (например, 'фэнтези'):")
    bot.register_next_step_handler(message, handle_genre)


def handle_genre(message):
    """
    Подбор книг по заданному жанру.
    """
    genre_name = message.text.strip()
    books = db.get_books_by_genre(genre_name)
    if books:
        response = f"Книги в жанре '{genre_name}':\n"
        for book in books:
            response += f"{book.name} - {book.price:.2f} руб. (Автор: {[author.name for author in book.authors]})\n"
    else:
        response = f"Книг в жанре '{genre_name}' не найдено."
    bot.reply_to(message, response)


@bot.message_handler(commands=['find_similar_books'])
def ask_for_similar_book_name(message):
    """
    Запрашивает у пользователя название книги для команды /find_similar_books.
    """
    bot.reply_to(message, "Введите название книги для поиска похожих (например, 'Гарри Поттер'):")
    bot.register_next_step_handler(message, handle_similar)


def handle_similar(message):
    """
    Подбор похожих книг по жанру с использованием готовой функции.
    """
    book_name = message.text.strip()
    similar_books = db.get_similar_books(book_name)

    if not similar_books:
        bot.reply_to(message, f"Похожих книг на '{book_name}' не найдено.")
        return

    # Форматируем результаты
    response = f"Похожие книги на '{book_name}':\n"
    for similar_book, similarity in similar_books[:5]:  # Ограничиваем вывод топ-5
        genres = ', '.join([genre.name for genre in similar_book.genres])
        authors = ', '.join([author.name for author in similar_book.authors])
        response += (
            f"- {similar_book.name} (Автор: {authors}, Жанры: {genres}) "
            f"- Сходство: {similarity:.2f}\n"
        )
    bot.reply_to(message, response)


if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)
