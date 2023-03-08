"""A web scraper that scrape image from Pinterest"""

from random import choice

import requests
import selenium.webdriver.support.expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

DESTINATION = "C:\\Users\\Damien\\Desktop\\DRAWING_\\Photo_ref"

OPTIONS = webdriver.ChromeOptions()
OPTIONS.add_argument("--start-maximized")
OPTIONS.add_argument("--incognito")


class Scraper:
    """Scraper"""
    def __init__(self):
        self.key_word = self.ask_key_word()
        self.image_amount = self.ask_amount()
        self.urls = set()

    def ask_key_word(self):
        """Ask for a valid sequence of word"""
        res = input("What image do you want to scrap?\n")
        while True:
            res = res.strip().replace(" ", "+")
            if res == "":
                res = input("Please enter valid key word:\n")
            else:
                return res

    def ask_amount(self):
        """Ask for an integer"""
        res = input("And how many?\n")
        while True:
            try:
                res = int(res)
                return res
            except ValueError:
                res = input("Please enter a valid number\n")

    def run(self):
        """
        Access google image search and scrap for
        the selected amount of images with selected keyword
        """
        driver = webdriver.Chrome(options=OPTIONS)
        wait = WebDriverWait(driver, 5)
        action = ActionChains(driver)
          
        driver.get("https://www.google.com/search?q="
                   f"{self.key_word}"
                   "+pinterest&source=lnms&tbm=isch&sa")
        # in case there is a cookie pop-up
        try:
            refuse_button = "//*[@id='yDmH0d']/c-wiz/div/div/div/div[2]/"\
                            "div[1]/div[3]/div[1]/div[1]/form[1]/div/div"\
                            "/button"
            wait.until(EC.presence_of_element_located((By.XPATH,
                                                       refuse_button)))
            driver.find_element(By.XPATH, refuse_button).click()
        except TimeoutException:
            pass

        thumbnails_path = "//*[@id='islrg']/div[1]/div/a[1]/div[1]/img"
        wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                        thumbnails_path)))

        thumbnails = driver.find_elements(By.XPATH,
                                          thumbnails_path)

        while len(self.urls) < self.image_amount:
            thumbnail = choice(thumbnails)
            action.move_to_element(thumbnail).click().perform()
            image_path = "//*[@id='Sva75c']/div[2]/div/div[2]/div[2]/div[2]"\
                         "/c-wiz/div/div[1]/div[2]/div[2]/div/a/img"
            try:
                wait.until(
                    EC.text_to_be_present_in_element_attribute((By.XPATH,
                                                                image_path),
                                                               "src",
                                                               "pinimg"))
            except TimeoutException:
                #the image was not from pinterest
                #or the url was not loaded
                continue

            image = driver.find_element(By.XPATH, image_path)
            print(image.get_attribute("src"))
            self.urls.add(image.get_attribute("src"))

        for image_url in self.urls:
            image_name = image_url.split("/")[-1]
            with open(f"{DESTINATION}\\{image_name}", "wb") as image_file:
                image_file.write(requests.get(image_url, timeout=10).content)


if __name__ == "__main__":
    Scraper().run()

