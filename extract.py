from config import *
import pandas as pd
from parser_utils import *
import pdb

def scrape_books_in_page(soup):
  books_table = soup.find_all("div", class_="elementList")
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

def extract_data(driver, soup):
  current_page = 1
  df = pd.DataFrame()

  while (has_next_page(soup)):
    current_url = URL + PAGE_URL_TEXT + str(current_page)
    driver.get(current_url)
    soup = soup_init(driver.page_source)
    data = scrape_books_in_page(soup)
    df = pd.concat([df, pd.DataFrame(data)], ignore_index=True)
    current_page += 1

  return df