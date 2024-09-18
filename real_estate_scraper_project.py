import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys


FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSePN1Xuy2xY0mCcblriDEB9CDIRS0yip1c9Q0pHzBjNInffeQ/viewform?usp=sf_link"

WEB_URL = "https://appbrewery.github.io/Zillow-Clone/"

#BEAUTIFUL SOUP
response = requests.get(WEB_URL)
rs_site = response.content

# print(rs_site)

soup = BeautifulSoup(rs_site,"html.parser")

listings = soup.find_all(name = "div" , class_ = "StyledPropertyCardDataWrapper")

links_list = []

for listing in listings:
    anchors = listing.find_all("a")
    for anchor in anchors:
        links_list.append(anchor.get("href"))

# print(links_list)

price_list = []
for listing in listings:
    prices = listing.find_all(name = "div", class_ = "PropertyCardWrapper")
    for price in prices:
        actual_price = price.text.strip()
        price_list.append(actual_price.strip("+ 1bd/mo"))

# print(price_list)

address_list = []
for listing in listings:
    addresses = listing.find_all("address")
    for address in addresses:
        actual_address = address.text.strip()
        address_list.append(actual_address.replace("| ",""))



if len(price_list) == len(address_list):
    print('You are going great')

#SELENIUM

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

driver = webdriver.Chrome(options=chrome_options)

for n in range(len(links_list)):
    driver.get(FORM_URL)
    time.sleep(2)

    XPATH_ADD = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'

    address_prop = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_ADD)))
    address_prop.send_keys(address_list[n])

    XPATH_PRICE = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'

    price_prop = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_PRICE)))
    price_prop.send_keys(price_list[n])

    XPATH_LINK = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'

    links_prop = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_LINK)))
    links_prop.send_keys(links_list[n])

    XPATH_BUTTON = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span'
    button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, XPATH_BUTTON)))
    button.click()


