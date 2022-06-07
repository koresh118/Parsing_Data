# Импортируем необходимые библиотеки и модули
import os
import time
from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import trange

# Объявляем переменные
date = ''
info_text = ''
likes = ''
reposts = ''
views = ''
post_link = ''
html = ''

# Метод извлечения даты поста
def get_date():
    global date
    get_date = get_post.find("span", class_="rel_date")
    date = get_date.get_text()

# Метод извлечения текста поста
def get_info():
    global info_text
    get_post_text = get_post.find("div", class_="wall_post_text")
    if (get_post_text == None):
        info_text = None
    else:
        info_text = get_post_text.get_text()

# Метод извлечения количества лайков и репостов
def get_likes():
    global likes
    global reposts
    get_likes = get_post.find_all("span", class_="PostBottomAction__count _like_button_count _counter_anim_container PostBottomAction__count--withBg")
    likes_list = []
    for like in get_likes:
        count = like.get_text()
        likes_list.append(count)
    likes = likes_list[0]
    reposts = likes_list[1]

# Метод извлечения количества просмотров
def get_views():
    global views
    get_views = get_post.find("span", class_="_views")
    views = get_views.get_text()
    views = views.replace("K", "000")

# Метод получения ссылки на пост
def get_link():
    global post_link
    get_id = get_post.parent
    id_ = get_id["id"]
    id_ = id_.replace("post-", "")
    post_link = f"https://vk.com/tokyofashion?w=wall-{id_}"

# Метод добавления данных в БД
def add_data():
    global post_link
    global date
    global views
    global reposts
    global likes
    global info_text
    posts.update_one({"Ссылка": post_link}, { "$set": {"Дата поста": date, "Содержание": info_text, "Поравилось": likes, "Поделились": reposts, "Просмотров": views}}, upsert=True)

# Метод "обнуления" данных
def zeroing_out():
    global post_link
    global date
    global views
    global reposts
    global likes
    global info_text
    date = ''
    info_text = ''
    likes = ''
    reposts = ''
    views = ''
    post_link = ''

# Метод "скроллинга" страницы
def scroll():
    global MAX_PAGE_NUMBER
    global html
    for i in trange(MAX_PAGE_NUMBER):
	    time.sleep(2)
	    posts = driver.find_elements_by_class_name("wall_post_text")
	    if not posts:
		    break
	    actions = ActionChains(driver)
	    actions.move_to_element(posts[-1])

	    actions.perform()
    html = driver.page_source


# Основные параметры
DRIVER_PATH = "./selenium_drivers/yandexdriver.exe"

url = "https://vk.com/tokyofashion"
headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36"
}

options = webdriver.ChromeOptions()

options.add_argument("--start-maximized")

driver = webdriver.Chrome(DRIVER_PATH, options=options)

MONGO_HOST = "localhost"
MONGO_PORT = 27017

# Запуск selenium
driver.get(url)

time.sleep(5)

# Переменная для метода скроллинга
MAX_PAGE_NUMBER = 1

# Делаем пробный скроллинг страницы, чтоб вызвать всплывающее окно
scroll()

time.sleep(3)

# Закрываем всплывающее окно
webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

# Делаем скроллинг для "удлиннения" HTML-кода, с целью получеиня большего количества постов
# Количество скроллингов (и, соответственно, - постов) может варьироваться 
# при помощи переменной MAX_PAGE_NUMBER
MAX_PAGE_NUMBER = 5
scroll()
# Запуск MongoDB
client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.posts_feed
posts = db.posts

# Запуск BeautifulSoup
#response = requests.get(url, headers=headers)
soup = BeautifulSoup(html, "html.parser")

# Запуск кода для парсинга постов
get_posts = soup.find_all("div", class_="_post_content")
for get_post in get_posts:
    get_info()
    if (info_text != None):
        get_date()
        get_likes()
        get_views()
        get_views()
        get_link()
        add_data()
        zeroing_out()

# Закрываем браузер
driver.quit()

# Закрываем клиент MongoDB
client.close
