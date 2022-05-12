# Импортируем необходимые библиотеки
import json
import requests
from bs4 import BeautifulSoup


# Добавляем словари и объявляем переменные
resp = {}
resp['vacancy'] = []
var = ""
tittle = ""
salary = ""
nameOrganization = ""
city = ""
link = ""
page = ""
n = 0
stage = 0


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

# Метод извлечения названия организации
def get_name_organization():
    global nameOrganization
    getNameOrganization = getVacancy.find("a", class_="bloko-link bloko-link_kind-tertiary")
    getNameOrganization = getNameOrganization.get_text(">", strip=False)
    nameOrganization = getNameOrganization.replace(">", "")

# Метод извлечения месторасположения организации
def get_city():
    global city
    getCity = getVacancy.find("div", class_="bloko-text bloko-text_no-top-indent")
    city = getCity.get_text(">", strip=False)

# Метод извлечения онлайн-ссылки на вакансию
def get_link():
    global link
    getLink = getVacancy.find("a", class_="bloko-link")
    link = getLink.get("href")

# Метод сохранения данных в словарь
def add_data():
    resp['vacancy'].append({
        'vacancy': tittle,
        'salary': salary,
        'org': nameOrganization,
        'place': city,
        'href': link,
        'link': 'https://hh.ru/'
    })

# Метод сохранения данных в json-файл
def save_all():
    with open('vacancy.json', 'w') as outfile:
        json.dump(resp, outfile)

# Основной код:
# Запрашиваем у пользователя название вакансии и приводим её к необходимому формату
var = input("Введите название вакансии: ")
var = var.replace(" ", "+")

# Запрашиваем у пользователя, сколько страниц из списка вакансий он хотел бы исследовать
n = int(input("Сколько страниц исследовать? "))

url = f"https://omsk.hh.ru/search/vacancy?text={var}&from=suggest_post&salary=&clusters=true&ored_clusters=true&enable_snippets=true&only_with_salary=true{page}"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36"
}

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
        add_data()
        save_all()
    
    stage = stage + 1
    page = f"&page={stage}&hhtmFrom=vacancy_search_list"
    url = url
