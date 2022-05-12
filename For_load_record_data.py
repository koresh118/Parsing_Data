# Импортируем необходимые библиотеки
import json

# Создаём метод, формирующий загруженные данные в удобный для восприятия формат
def load_data(getVacancy):
    for n in getVacancy['vacancy']:
        print("Вакансия:", n['vacancy'])
        print("Заработная плата:", n['salary'])
        print("Организация:", n['org'])
        print("Город:", n['place'])
        print("Ссылка:", n['href'])
        print("Откуда взята вакансия:", n['link'])
        print("-"*50)

# Загружаем JSON-файл
with open('vacancy.json') as json_file:
    getVacancy = json.load(json_file)

# Выводим данные на экран
print(load_data(getVacancy))
