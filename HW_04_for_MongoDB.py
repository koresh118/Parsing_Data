import requests
import csv
from pprint import pprint
from lxml.html import fromstring
from datetime import date
from bson import ObjectId
from pymongo import ASCENDING, DESCENDING, MongoClient

MONGO_HOST = "localhost"
MONGO_PORT = 27017

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client.news_feed
news = db.news

def add_data():
    global tittle
    global time
    global link
    global source
    news.update_one({"Ссыдка": link}, { "$set": {"Тезис": tittle, "Время публикации": time, "Ссыдка": link, "Источник": source}}, upsert=True)

def zeroing_out():
    global tittle
    global time
    global link
    tittle = ""
    time = ""
    link = ""

url = "https://lenta.ru/"

headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" 
	"AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.141 YaBrowser/22.3.3.852 Yowser/2.5 Safari/537.36"
}

topic_patch = '//div[contains(@class, "topnews")]//*[contains(@class, "card-big _topnews _news")]'
allNews_patch = '//div[@class="main-container"]//a/*[contains(@class, "card-mini__text")]'
source = "Лента.ру"
topicText_patch = '//div[contains(@class, "topnews")]//h3[contains(@class, "card-big__title")]//text()'
topicLink_patch = '//a[@class="card-big _topnews _news"]/@href'
topicTime_patch = '//div[contains(@class, "topnews")]//*[contains(@class, "card-big _topnews _news")]//time//text()'
allNewsText_patch = '//div[@class="main-container"]//*[@class="card-mini__title"]//text()'
allNewsLink_patch = '//div[contains(@class, "main-container")]//*[contains(@class, "card-mini")]//@href'
allNewsTime_patch = '//div[contains(@class, "main-container")]//*[contains(@class, "card-mini")]//time//text()'
date = date.today()

response = requests.get(url, headers=headers)
dom = fromstring(response.text)

tittle = dom.xpath(topicText_patch)
tittle = tittle[0]
time = dom.xpath(topicTime_patch)
time = time[0]
time = f"{date}, {time}"
link = dom.xpath(topicLink_patch)
link = link[0]
link = "https://lenta.ru" + link
add_data()

allTittle = dom.xpath(allNewsText_patch)
allTime = dom.xpath(allNewsTime_patch)
allLinks = dom.xpath(allNewsLink_patch)
coin = len(allTittle)

allNews = dom.xpath(allNews_patch)
numbers = len(allNews)
for n in range(numbers):
    tittle = allTittle[n]
    time = allTime[n]
    time = f"{date}, {time}"
    link = allLinks[n]
    link = "https://lenta.ru" + link
#    new = {"Тезис": tittle, "Время публикации": time, "Ссыдка": link, "Источник": source}
    add_data()

#    news.update_one({"Ссыдка": link}, { "$set": {"Тезис": tittle, "Время публикации": time, "Ссыдка": link, "Источник": source}}, upsert=True)
    zeroing_out()
    n = n + 1
client.close

