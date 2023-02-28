import requests
from time import sleep
from random import choice, randint
from selenium import webdriver
from bs4 import BeautifulSoup

# where the images should be saved
IMAGE_PATH = "C:/Users/Damien/Desktop/DRAWING_/Photo_ref"

SEARCH = ["kan liu", "sam does art", "ross draws", "ilya kushinov", "wlop art",
          "colorful anime art"]


def main(search):

    search: str

    search = search.strip().replace(' ', '%20')
    DRIVER = webdriver.Chrome()
    # we have to use selenium because the images won't load with request
    DRIVER.get(f"https://www.pinterest.fr/search/pins/?q={search}&rs=typed")

    DRIVER.maximize_window()  # to load more images on screen
    sleep(3)

    for _ in range(randint(0, 10)):
        DRIVER.execute_script("window.scrollBy(0, 500)", "")
        sleep(0.1)

    soup = BeautifulSoup(DRIVER.page_source, "html.parser")

    # get all the links to all the pins present on screen
    links = []
    for element in soup.find_all("a", href=True):
        if "/pin/" in element["href"]:
            links.append(element["href"])

    # we don't need to load the page with selenium
    page_source = requests.get(f"https://www.pinterest.fr{choice(links)}")
    soup = BeautifulSoup(page_source.content, "html.parser")
    image_url = soup.find("img", src=True)["src"]

    image_name = image_url.split("/")[-1]

    # save the image if the image is a jpg
    if image_name.endswith(".jpg"):
        with open(f"{IMAGE_PATH}/{image_name}", "wb") as image_file:
            image_file.write(requests.get(image_url).content)
    else:
        print("the image was a png")

    DRIVER.quit()


if __name__ == "__main__":

    for _ in range(5):
        main(choice(SEARCH))
