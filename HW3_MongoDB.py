# Импортируем необходимые библиотеки
import json
import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint
from bson import ObjectId
from pymongo import MongoClient

# Добавляем словари и объявляем переменные
resp = {}
resp['vacancy'] = []
var = ""
tittle = ""
salary = ""
count_salary = ""
level_salary = 0
nameOrganization = ""
city = ""
link = ""
page = ""
n = 0
a = ""
stage = 0
only_fresh = ""

# Назначаем параметры для работы с MongoDB
MONGO_HOST = "localhost"
MONGO_PORT = 27017

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.list_of_vacancies
job = db.job

# Метод извлечения названия вакансии
def get_vacancy_name():
    global tittle
    getVacancyName = getVacancy.find(attrs={"target": "_blank"})
    tittle = getVacancyName.get_text(">", strip=False)

# Метод извлечения уровня заработной платы
def get_salary():
    global salary
    getSalary = getVacancy.find("span", class_="bloko-header-section-3")
    getSalary = getSalary.get_text(">", strip=False)
    salary = getSalary.replace(" >", " ")

# Метод вывода на экран вакансий, у которых уровень заработной платы выше заданного значения
def get_level_salary():
    global salary
    global count_salary
    global level_salary
    global tittle
    global nameOrganization
    global city
    global link
    salary1 = ""
    countSalary = salary.replace(" ", "")
    for c in countSalary:
        if c.isdigit():
            salary1 = salary1 + c
        elif ((c == ">") or (c == "–")):
            break
    count_salary = int(salary1)
    salary1 = ""
    if (count_salary > level_salary):
        print("*" * 80)
        print(f"""Вакансия: {tittle}
Зарплата: {salary}
Организация: {nameOrganization}
Город: {city}
Ссылка: {link}""")
    count_salary = ""

# Метод извлечения названия организации
def get_name_organization():
    global nameOrganization
    getNameOrganization = getVacancy.find("a", class_="bloko-link bloko-link_kind-tertiary")
    getNameOrganization = getNameOrganization.get_text(">", strip=False)
    nameOrganization = getNameOrganization.replace(">", "")

# Метод извлечения месторасположения организации
def get_city():
    global city
    global a
    getCity = getVacancy.find("div", class_="bloko-text bloko-text_no-top-indent")
    city = getCity.get_text(">", strip=False)
    city = str(city)
    for i in city:
        a = a + i
        if (i == ">"):
            break
    a = a.replace(">", "")
    city = a
    a = ""

# Метод извлечения онлайн-ссылки на вакансию
def get_link():
    global link
    getLink = getVacancy.find("a", class_="bloko-link")
    link = getLink.get("href")

# Метод "обнуления" данных
def zeroing_out():
    global tittle
    global salary
    global nameOrganization
    global city
    global link
    tittle = ""
    salary = ""
    nameOrganization = ""
    city = ""
    link = ""

# Метод для записи данных в файл
def add_data():
    global tittle
    global salary
    global nameOrganization
    global city
    global link
    job.update_one({"Ссылка": link}, { "$set": {"Название": tittle, "Зарплата": salary, "Ссылка": link, "Организация": nameOrganization, "Город": city}}, upsert=True)

# Метод перехода на следующую страницу
def next_page():
    global stage
    global page
    global url
    stage = stage + 1
    page = f"&page={stage}&hhtmFrom=vacancy_search_list"

# Основной код:
# Запрашиваем у пользователя название вакансии и приводим её к необходимому формату
var = input("Введите название вакансии: ")
var = var.replace(" ", "+")


# Запрашиваем у пользователя, сколько страниц из списка вакансий он хотел бы исследовать
n = int(input("Сколько страниц исследовать? "))

url = f"https://hh.ru/search/vacancy?text={var}&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&only_with_salary=true{page}"
    
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36"
}

# Запрашиваем уровень заработной платы
level_salary = int(input("Какой размер заработной платы Вас интересует? "))

# Основной цикл программы
for one_page in range(n):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    getAllVacancy = soup.find_all("div", class_="vacancy-serp-item__layout")
    for getVacancy in getAllVacancy:
        get_vacancy_name()
        get_salary()
        get_name_organization()
        get_city()
        get_link()
        get_level_salary()
        add_data()
        zeroing_out()

    next_page()
    url = url

client.close
