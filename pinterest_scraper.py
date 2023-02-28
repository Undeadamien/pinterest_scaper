import requests
from time import sleep
from random import choice
from selenium import webdriver
from bs4 import BeautifulSoup

SEARCH = ["kan liu", "sam does art", "ross draws", "ilya kushinov", ]
DRIVER = webdriver.Chrome()

key_words = choice(SEARCH)
key_words = key_words.strip()
key_words = key_words.replace(" ", "%20")

DRIVER.get(f"https://www.pinterest.fr/search/pins/?q={key_words}&rs=typed")
DRIVER.maximize_window()
sleep(2)
soup = BeautifulSoup(DRIVER.page_source, "html.parser")

links = []
for element in soup.find_all("a", href=True):
    if "/pin/" in element["href"]:
        links.append(element["href"])

DRIVER.get(f"https://www.pinterest.fr{choice(links)}")
soup = BeautifulSoup(DRIVER.page_source, "html.parser")
image_url = soup.find("img", src=True)["src"]


splited_image_url = image_url.split("/")
image_name = splited_image_url[-1]
print(image_name)

if image_name.endswith("jpg"):
    with open(image_name, "wb") as image_file:
        image_file.write(requests.get(image_url).content)

DRIVER.quit()
