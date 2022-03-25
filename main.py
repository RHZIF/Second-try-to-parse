import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
# your skills are actually very good

def get_data(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"
    }

    r = requests.get(url=url, headers=headers)

    with open("index.html", "w", encoding='utf-8') as file:
        file.write(r.text)

    r = requests.get('https://api.rsrv.me/hc.php?a=hc&most_id=1317&l=ru&sort=most',
                     headers=headers)
    soup = BeautifulSoup(r.text, "lxml")

    hotels_cards = soup.find_all("div", class_="hotel_card_dv")

    url_lst = []
    for hotel_url in hotels_cards:
        hotel_url = hotel_url.find("a").get("href")
        url_lst.append(hotel_url)

    with open(file='url.txt', mode='w') as file:
        for url in url_lst:
            file.write(f'{url}\n')

    return 'Work done!'


def get_data_with_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                         "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36")

    try:
        driver = webdriver.Chrome(options=options)
        driver.get(url=url)
        time.sleep(5)

        with open(file="index_selenium.html", mode="w", encoding='utf-8') as file:
            file.write(driver.page_source)

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    with open(file="index_selenium.html", mode='r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")

    hotels_cards = soup.find_all("div", class_="hotel_card_dv")

    url_lst = []
    for hotel_url in hotels_cards:
        hotel_url = "https://www.tury.ru" + hotel_url.find("a").get("href")
        url_lst.append(hotel_url)

    with open(file='url_selenium.txt', mode='w') as file:
        for url in url_lst:
            file.write(f'{url}\n')

    return 'Work done!'


def main():
    # get_data("https://www.tury.ru/hotel/most_luxe.php")
    get_data_with_selenium("https://www.tury.ru/hotel/most_luxe.php")


if __name__ == '__main__':
    main()
