## Отчёт на КТ-2:

Что есть из того что мы хотели сделать:
Напоминаю что мы хотели сделать веб-сервис с помощью которого можно было бы 
а) сравнивать цены на книжки на разных сайтах
б) получать рекомендии

Что у нас есть сейчас:

У нас есть тг-бот,  @book_price_comparer_bot, запускается файлом telegram_bot.py
При запуске запускается initial_parse.py, там лежат настройки для изначального парсинга при подъеме бота.
Сейчас в том скрипте изначального парсинга лежит первые N страниц с Читай-города. Про парсинг подробнее отдельно.
Скрипт парсит Читай-город и отправляет данные оттуда в базу данных, которая создается файликом books.db
Работа DB описывается в Data_Base.py

Каждую спаршенную с ЧГ книжку мы ищем на LiveLib (Аналог кинопоиска для книжек), логика прописана в livelib.py и пытаемся спарсить отттуда теги. В данный момент это не всегда удается, так как после многих тестов LiveLib что-то понял и внёс меня в список роботов, поэтому мне открывается страница отличная от той что я хотел бы чтобы открывалась на Livelib. Я думаю если запускать в первый раз, то теги с LiveLib спарсятся. 
Протестить можно в query_tags.py, скрипт просто выводит найденные теги (жанры) в консоль.

БД устроена так: есть три важные таблицы books, authors, genre; их связь устроена как многие к многим между books<->authors и books<->genre(с добавлением соответствующих таблиц book_authors и book_genres). Наша БД поддерживает добавление и удаление книжек по их названию, а также можно выполнять GET по имени книжки, автора или жанра(вовыдится будет все подходящие книжки). Вместе с тем БД поддерживает простое хранение файле в PC или можно хранить на своем docker сервере(в нашем случае просто localhost).  Планируется добавить мониторинг сервера где хранится ДБ(если успеется и посчитается нужным), а также добавить рекомендации (реализованные через определенную метрику или через AI).
Работа DB описывается в Data_Base.py

После чего бот командами 
/find_book_by_name 
/find_book_by_author
/find_book_by_genre
делает запросы к бд и выводит книжки которые лежат в дб пользователю.
В будущем хотим добавить чтобы в случае ненахождения книжки делался отдельный запрос к каждому из сайтов, логика что-то типа того что сейчас в query_script лежит.
Работа описывается бота в telegram_bot.py

Насчёт парсинга
Сейчас полноценно сделан только парсинг Читай-Города в chitaigorod.py. Он может парсить с страниц по порядку + таргетно парсить книжки по запросу, в query_script можно найти пример этого
Ещё частично сделаны bukvoed.py и labirint.py, они могут только парсить со страниц по порядку.
mif.py может парсить первые 50 книжек с главной, потом он упирается в кнопки джаваскрипта, которые пока прожимать не умеет.

Каждый сайт сделан в виде scrapy.Spider, который может быть настроен на один из двух пайплайнов из Bookparser.py
DBPipeline записывает книжки в базу данных
CSVPipeline, который стоит в пауках по умолчанию записывает результаты парсинга в CSV файл

Ещё в test_Data_Base.py лежат тесты для Data_Base.py