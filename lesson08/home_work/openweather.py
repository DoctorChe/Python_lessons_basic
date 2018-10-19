"""
== OpenWeatherMap ==

OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.

Необходимо решить следующие задачи:

== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.
    
    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID, 
    используя дополнительную библиотеку GRAB (pip install grab)

        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up

        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in

        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys
        
        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

        
== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz
    
    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка 
     (воспользоваться модулем gzip 
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)
    
    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}
    
    
== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a

    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a

    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a


    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}    


== Сохранение данных в локальную БД ==    
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):

    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных

2. Выводить список стран из файла и предлагать пользователю выбрать страну 
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))

3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.


При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.


При работе с XML-файлами:

Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>

Чтобы работать с пространствами имен удобно пользоваться такими функциями:

    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''

    tree = ET.parse(f)
    root = tree.getroot()

    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}

    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...

"""

import urllib
import urllib.request
import gzip
import json
import sqlite3
from pathlib import Path

DB_PATH = "database.db"
JSON_PATH = "city.list.json"


def get_appid():
    with open("app.id", "r") as f:
        appid = f.read()
    return appid


def get_cities_archive():
    destination_gz = JSON_PATH + ".gz"
    city_list_json_gz_file = Path(destination_gz)
    if city_list_json_gz_file.is_file():
        print("Файл со списком городов существует")
    else:
        url = "http://bulk.openweathermap.org/sample/city.list.json.gz"
        # destination_gz = "city.list.json.gz"
        # destination_json = "city.list.json"
        urllib.request.urlretrieve(url, destination_gz)
        # gzip.decompress(destination)
        with gzip.open(destination_gz, "rb") as fin:
            # with open(destination_json, "wb") as fout:
            with open(JSON_PATH, "wb") as fout:
                fout.write(fin.read())


def get_weather(d):
    params = urllib.parse.urlencode(d)
    url = f"http://api.openweathermap.org/data/2.5/weather?{params}"
    with urllib.request.urlopen(url) as f:
        json_string = f.read().decode('utf-8')
        parsed_string = json.loads(json_string)
        return {
            "id_города": parsed_string['id'],
            "Город": parsed_string['name'],
            "Дата": parsed_string['dt'],
            "Температура": parsed_string['main']['temp'],
            "id_погоды": parsed_string['weather'][0]['id']
        }


def get_countries():
    countries = set()
    with open(JSON_PATH, "r", encoding="UTF-8") as json_data:
        cities = json.load(json_data)
    for city in cities:
        countries.add(city["country"])
    return countries


def get_cities(country):
    cities_in_country = set()
    with open(JSON_PATH, "r", encoding="UTF-8") as json_data:
        cities = json.load(json_data)
    for city in cities:
        if city["country"] == country:
            cities_in_country.add(city["name"])
    return cities_in_country


def find_city(**kwargs):
    with open(JSON_PATH, "r", encoding="UTF-8") as json_data:
        cities = json.load(json_data)
    for city in cities:
        if city["name"] == kwargs["name"] and city["country"] == kwargs["country"]:
            return city["id"]


def make_db_file():
    db_file = Path(DB_PATH)
    if db_file.is_file():
        print("Файл базы данных существует")
    else:
        try:
            file = open(DB_PATH, 'w')
            print("Файл базы данных содан")
            file.close()
        except IOError:
            print("Не удалось создать файл базы данных")


class DataConn:
    """
    Класс Context Manager
    Создает связь с базой данных SQLite и закрывает её по окончанию работы
    """

    def __init__(self, db_name):
        """Конструктор"""
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Открываем подключение к базе данных"""
        self.conn = sqlite3.connect(self.db_name)
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Закрываем подключение"""
        self.conn.close()
        if exc_val:
            raise Exception


def create_table():
    """Создание базы данных"""
    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()
            # Создание таблицы "Погода"
            cursor.execute("""
                              CREATE TABLE IF NOT EXISTS weather
                              (id_города INTEGER PRIMARY KEY,
                              Город VARCHAR(255),
                              Дата DATE,
                              Температура INTEGER,
                              id_погоды TEXT)
                           """)


def copy_from_json_to_db(weather):
    """Запись данных в базу данных"""

    # id_города = weather["id_города"]
    # Город = weather["Город"]
    # Дата = weather["Дата"]
    # Температура = weather["Температура"]
    # id_погоды = weather["id_погоды"]

    weather_insert = (
        weather["id_города"],
        weather["Город"],
        weather["Дата"],
        weather["Температура"],
        weather["id_погоды"],
    )
    weather_update = (
        weather["Город"],
        weather["Дата"],
        weather["Температура"],
        weather["id_погоды"],
        weather["id_города"],
    )

    sql = (
           "SELECT * FROM weather WHERE id_города=?",
           "INSERT INTO weather VALUES (?,?,?,?,?)",
           "UPDATE weather SET Город=?, Дата=?, Температура=?, id_погоды=? WHERE id_города=?",
           )

    # conn = sqlite3.connect(DB_PATH)
    # cursor = conn.cursor()
    # cursor.execute(sql[0], [id_города, ])
    # if not cursor.fetchall():  # проверка на существование идентичной записи
    #     print("Данных не существует, вносим данные")
    #     cursor.execute(sql[1], weather)  # Внесение данных в таблицу
    # else:
    #     print("Данные существуют, изменяем данные")
    #     cursor.execute(sql[2], (Город, Дата, Температура, id_погоды, id_города))  # Изменение данных в таблице
    #
    # cursor.close()
    # conn.close()

    with DataConn(DB_PATH) as conn:
        with conn:
            cursor = conn.cursor()
            create_table()  # Создать таблицу, если не существует
            cursor.execute(sql[0], (weather["id_города"], ))
            if not cursor.fetchall():  # проверка на существование идентичной записи
                print("Данных не существует, вносим данные")
                cursor.execute(sql[1], weather_insert)  # Внесение данных в таблицу
            else:
                print("Данные существуют, изменяем данные")
                cursor.execute(sql[2], weather_update)  # Изменение данных в таблице

            cursor.execute("SELECT * FROM weather")
            print(cursor.fetchall())

    # query = """
    #     INSERT INTO weather (id_города, Город, Дата, Температура, id_погоды)
    #         VALUES(id_города, Город, Дата, Температура, id_погоды)
    #         ON CONFLICT(id_города)
    #         DO UPDATE SET (
    #         Город=excluded.Город,
    #         Дата=excluded.Дата,
    #         Температура=excluded.Температура,
    #         id_погоды=excluded.id_погоды
    #         );
    # """

    # weather = json.load(open(JSON_PATH))
    # db = sqlite3.connect(DB_PATH)
    # query = "INSERT OR IGNORE INTO weather VALUES (?,?,?,?,?)"
    # # query = """
    # #     INSERT INTO weather (user_name, age)
    # #         VALUES('steven', 32)
    # #         ON CONFLICT(user_name)
    # #         DO UPDATE SET age=excluded.age;"""
    # columns = ['id_города', 'Город', 'Дата', 'Температура', 'id_погоды']
    # for data in weather():
    #     keys = tuple(data[col] for col in columns)
    #     c = db.cursor()
    #     c.execute(query, keys)
    #     c.close()


if __name__ == "__main__":
    make_db_file()
    get_cities_archive()
    countries = sorted(get_countries())
    print(countries)
    while True:
        country = input("Введите название стараны из списка: ")
        if country in countries:
            break
    cities = sorted(get_cities(country))
    print(cities)
    while True:
        city = input("Введите название города из списка: ")
        if city in cities:
            break
        else:
            match_cities = []
            for c in cities:
                if c.startswith(city):
                    match_cities.append(c)
            if match_cities:
                if len(match_cities) == 1:
                    city = match_cities[0]
                    break
                else:
                    print(f"Список подходящих городов:\n{match_cities}")
            else:
                print("Не найдено такого города")
    city_id = find_city(name=city, country=country)
    # city_id = find_city(name="State of Haryāna", country="IN")
    d = {}  # Словарь с параметрами для запроса погоды
    d["appid"] = get_appid()
    d["id"] = city_id
    d["units"] = "metric"
    # get_weather(d)
    weather = get_weather(d)
    print(weather)
    copy_from_json_to_db(weather)
