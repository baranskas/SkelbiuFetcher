from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import time
from playsound import playsound
import os
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *

# TO DO
# - PROFITABILITY ALGORITHM (compares price to 3-5 similar products)

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

fetched_ids_skelbiu = []

def start_checker(links):
    for i in links:
        driver.get(i)
        products = driver.find_elements(By.CLASS_NAME, "standard-list-item")
        for product in products:
            if product.get_attribute("data-item-id") not in fetched_ids_skelbiu:
                fetched_ids_skelbiu.append(product.get_attribute("data-item-id"))

links = []

kompiuterija_link = 'https://shorturl.at/cwxMO'
komunikacijos_link = 'https://shorturl.at/fgqtD'
technika_link = 'https://shorturl.at/hGHU2'
ismanieji_link = 'https://shorturl.at/jpAE6'
visi_link = 'https://t.ly/UR0nu'
steam_deck_link = 'https://www.skelbiu.lt/skelbimai/?autocompleted=1&keywords=steam+deck&cities=0&distance=0&mainCity=0&search=1&category_id=0&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=1&detailsSearch=0'
foto_link = 'https://www.skelbiu.lt/skelbimai/?autocompleted=1&keywords=&cost_min=&cost_max=&type=0&condition=&cities=0&distance=0&mainCity=0&search=1&category_id=248&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=1&detailsSearch=1'
phone_link = 'https://www.skelbiu.lt/skelbimai/?autocompleted=1&keywords=&cost_min=&cost_max=&type=0&condition=&cities=0&distance=0&mainCity=0&search=1&category_id=63&user_type=0&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=1&detailsSearch=0'

def append_if_not_appended(link):
    if link not in links:
        links.append(link)

def link(uri, label=None):
    if label is None:
        label = uri
    parameters = ''
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)

os.system('cls' if os.name == 'nt' else 'clear')

svetaine = "Skelbiu"

sound_options = [
        "Sound On",
        "Sound Off",
]

sound = select(sound_options, cursor="🢧", cursor_style="cyan")

sound_bool = True

if sound == "Sound On":
    sound_bool = True
else:
    sound_bool = False

if svetaine == "Skelbiu":
    item_options = [
            "Komunikacija",
            "Kompiuterija",
            "Technika",
            "Išmanieji laikrodžiai",
            "Visi",
            "Steam Deck",
            "Fotoaparatai",
            "Mobilieji Telefonai",
    ]

    items = select_multiple(item_options, tick_character='✅', ticked_indices=[0], maximal_count=5, minimal_count=1)

if "Komunikacija" in items:
    append_if_not_appended(komunikacijos_link)

if "Kompiuterija" in items:
    append_if_not_appended(kompiuterija_link)

if "Technika" in items:
    append_if_not_appended(technika_link)

if "Išmanieji laikrodžiai" in items:
    append_if_not_appended(ismanieji_link)

if "Steam Deck" in items:
    append_if_not_appended(steam_deck_link)

if "Fotoaparatai" in items:
    append_if_not_appended(foto_link)

if "Mobilieji Telefonai" in items:
    append_if_not_appended(phone_link)

if "Visi" in items:
    links = []
    append_if_not_appended(visi_link)

start_checker(links)

spinner = Spinner(DOTS, "Laukiama skelbimų...")
spinner.start()

while True:
    # driver.get(url)
    for i in links:
        driver.get(i)

        products = driver.find_elements(By.CLASS_NAME, "standard-list-item")

        for product in products:
            if product.get_attribute("data-item-id") not in fetched_ids_skelbiu:

                now = datetime.now()
                current_time = now.strftime("%H:%M")

                title = product.find_element(By.CLASS_NAME, "extended-info").find_element(By.CLASS_NAME, "content-block").find_element(By.CLASS_NAME, "title").text

                price_parent = product.find_element(By.CLASS_NAME, "price-line")

                city = product.find_element(By.CLASS_NAME, "second-dataline").text.split(",")[0]

                fetched_ids_skelbiu.append(product.get_attribute("data-item-id"))

                link_url = product.get_attribute("href")

                try:
                    price = price_parent.find_element(By.CLASS_NAME, "price").text
                    print("{0:<50} | {1:>7} | {2:>15} | {3:>2} | {4:>3}".format(title, price, city, link(link_url, "Nuoroda"), current_time))

                    if sound_bool:
                        playsound('bing.wav')
                except:
                    print("{0:<50} | {1:>7} | {2:>15} | {3:>2} | {4:>3}".format(title, "NoPrice", city, link(link_url, "Nuoroda"), current_time))

        time.sleep(5)