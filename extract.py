"""Provides methods to extract the data through scraping."""
import pandas as pd
import numpy as np
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import config
import parser_utils

def scrape_books_in_page(soup, debug):
    books_table = soup.find_all("div", class_="elementList")
    if debug:
        del books_table[2:]

    data = []
    for e in books_table:
        title = e.find("a", class_="bookTitle")
        author = e.find("a", class_="authorName")
        additional_text = e.find("span", class_="greyText smallText")

        if title:
            book = {
                "title": title.text,
                "author": author.text,
                "additional_text": additional_text.text,
                "url": title.get("href")
            }
            data.append(book)
    return data

def has_next_page(soup):
    return bool(soup.find("a", class_="next_page"))

def fetch_general_infos(driver, debug, shelf):
    current_page = 1
    df = pd.DataFrame()
    shelf_url = config.URL + shelf
    while True:
        print(f"Scraping page: {current_page}")
        current_url = shelf_url + config.PAGE_URL_TEXT + str(current_page)
        driver.get(current_url)
        soup = parser_utils.soup_init(driver.page_source)
        data = scrape_books_in_page(soup, debug)
        df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
        if debug:
            condition = current_page <= 1
        else:
            condition = has_next_page(soup)
        if not condition:
            break
        current_page += 1

    return df

def fetch_book_page(book, driver):
    print(f"Scraping book: {book.title}")
    detailed_page_url = config.BASE_URL + book.url
    driver.get(detailed_page_url)
    delay = 10
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="currentlyReadingSignal"]'))
        )
    except TimeoutException:
        print(f"Timeout on book page. Some information might be missing for this book: {book.title}")

def fetch_detailed_infos(book, driver):
    fetch_book_page(book, driver)
    soup = parser_utils.soup_init(driver.page_source)

    page_count_el = soup.find("p", {'data-testid': 'pagesFormat'})
    page_count = np.nan if not page_count_el or not hasattr(page_count_el, "text") else page_count_el.text

    shop_button = soup.find("button", class_="Button--buy")
    price = np.nan if not shop_button or not hasattr(shop_button, "text") or shop_button.text.startswith("Shop") else shop_button.text

    currently_reading_count_el = soup.find("div", {'data-testid': 'currentlyReadingSignal'})
    currently_reading_count = np.nan if not currently_reading_count_el or not hasattr(currently_reading_count_el, "text") else currently_reading_count_el.text

    wanting_to_read_count_el = soup.find("div", {'data-testid': 'toReadSignal'})
    wanting_to_read_count = np.nan if not wanting_to_read_count_el or not hasattr(wanting_to_read_count_el, "text") else wanting_to_read_count_el.text

    return pd.Series({
        "page_count": page_count,
        "price": price,
        "currently_reading_count": currently_reading_count,
        "wanting_to_read_count": wanting_to_read_count
    })

def extract_data(driver, debug, shelf):
    basics_df = fetch_general_infos(driver, debug, shelf)
    fetch_detailed_infos_lambda = lambda book: fetch_detailed_infos(book, driver)
    dtl_inf_col_names = ["page_count", "price", "currently_reading_count", "wanting_to_read_count"]
    basics_df[dtl_inf_col_names] = basics_df.apply(
        fetch_detailed_infos_lambda,
        axis=1,
        result_type='expand'
    )
    return basics_df