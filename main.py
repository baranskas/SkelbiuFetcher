from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

fetched_listing_id = []

# Link input, splitting and optimising for easier page iteration
starter_link = "https://www.skelbiu.lt/skelbimai/?autocompleted=1&orderBy=1&keywords="
search_link = (starter_link + input("Search for an item to scrape for: ")).replace(" ", "-")


def link_format(uri, label=None):  # Necessary for links to work in terminals
    if label is None:
        label = uri
    parameters = ''
    escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
    return escape_mask.format(parameters, uri, label)


while True:
    driver.get(search_link)
    for listing in search_link:
        listings = driver.find_elements(By.CLASS_NAME, "standard-list-item")
        for product in listings:
            if product.get_attribute("data-item-id") not in fetched_listing_id:
                title = product.find_element(By.CLASS_NAME, "extended-info").find_element(By.CLASS_NAME, "content-block").find_element(By.CLASS_NAME, "title").text
                city = product.find_element(By.CLASS_NAME, "second-dataline").text.split(",")[0]
                fetched_listing_id.append(product.get_attribute("data-item-id"))
                link_url = product.get_attribute("href")
                try:
                    price = product.find_element(By.CLASS_NAME, "price-line").find_element(By.CLASS_NAME, "price").text
                    print("{0:<50} | {1:>10} | {2:>15} | {3:>2}".format(title, price, city, link_format(link_url, "Link")))
                except:
                    print("{0:<50} | {1:>10} | {2:>15} | {3:>2}".format(title, "NoPrice", city, link_format(link_url, "Link")))
