import requests

user_data = {}

print('Добро пожаловать на поисковик фильмов! '
      '\nПрограмма работает на основе кинопоиска, '
      'и на данный момент поддерживает поиск по трем параметрам. \nИтак, давайте начнем!')
# Проверка ввода рейтинга
def check_age():
    while True:
        rating = input("Введите минимальный возраст, при котором можно смотреть фильм (от 0 до 18): ")
        if rating.isdigit() and 0 <= int(rating) <= 18:
            break
        else:
            print("Введенное значение должно быть в диапазоне от 0 до 18. Пожалуйста, попробуйте снова.")
    return rating


# Проверка ввода года
def check_year():
    while True:
        year = input("Введите минимальный год выпуска фильма (от 1900 до 2023): ")
        if year.isdigit() and 1900 <= int(year) <= 2023:
            break
        else:
            print("Введенное значение должно быть в диапазоне от 1900 до 2023. Пожалуйста, попробуйте снова.")
    return year


def check_length():
    # Проверка ввода продолжительности
    while True:
        length = input("Введите минимальную продолжительность фильма в минутах (от 60 до 300): ")
        if length.isdigit() and 60 <= int(length) <= 300:
            break
        else:
            print("Введенное значение должно быть в диапазоне от 60 до 300. Пожалуйста, попробуйте снова.")
    return length


user_data['genre'] = input('Пожалуйста, введите жанр фильма, который вы хотите найти: ')
user_data['rating'] = check_age()
user_data['year'] = check_year()
user_data['duration'] = check_length()


def check_input():
    while True:
        inp = input("Введите 1, чтобы перейти на следующую страницу, или 0, чтобы прекратить поиск: ")
        if inp in ['0', '1']:
            break
        else:
            print("Введенное значение должно быть 0 или 1. Пожалуйста, попробуйте снова.")
    return inp


# Отправка запроса на фильтрацию фильмов
headers = {
    "X-API-KEY": "ZKXFTB9-A2T4VRS-K1TTF8N-55MGYKV"
}

params = {
    'genres.name': user_data['genre'],
    'ageRating': user_data['rating'],
    'year': f"{user_data['year']}-2023",
    'movieLength': user_data['duration'],
    'limit': 50,
    'page': 1
}

response = requests.get('https://api.kinopoisk.dev/v1.3/movie', params=params, headers=headers, stream=True)

response.raise_for_status()

films = response.json()

print('Итак, вот список из фильмов, которые удовлетворяют вашим запросам:')
current_page = 1
next_page = True

while next_page:
    try:
        print(f"Страница {current_page}:")
        for i, film in enumerate(films['docs'], start=1):
            if film["name"] is not None:
                link = 'Отсутствует'
                if film["watchability"]['items'] is not None:
                    link = film["watchability"]['items'][0]['url']
                print(f'Название: {film["name"]}')
                print(f'Описание: {film["description"]}')
                print(f'Год выпуска: {film["year"]}')
                print(f'Ссылка: {link}')
                print()

        user_input = check_input()
        if user_input == '1':
            current_page += 1
            params['page'] = current_page
            response = requests.get('https://api.kinopoisk.dev/v1.3/movie', params=params, headers=headers, stream=True)
            films = response.json()
        else:
            next_page = False
    except Exception as E:
        print('К сожалению, что-то пошло не так и поиск сломался. Приносим свои извинения.')

print("Поиск завершен.")

for i, film in enumerate(films['docs'], start=1):
    if film["name"] is not None:
        link = 'Отсутствует'
        if film["watchability"]['items'] is not None:
            link = film["watchability"]['items'][0]['url']
        print(f'Название: {film["name"]}')
        print(f'Описание: {film["description"]}')
        print(f'Год выпуска: {film["year"]}')
        print(f'Ссылка: {link}')
        print()

# import requests
#
# url = 'https://api.kinopoisk.dev/v1.3/movie'
# api = 'ZKXFTB9-A2T4VRS-K1TTF8N-55MGYKV'
#
# print(requests.get(url=url, ))























