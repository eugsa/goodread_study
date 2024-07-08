from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import pdb
import os
from dotenv import load_dotenv

HEADERS = {
  "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
  "Cache-Control": "no-cache",
  "Pragma": "no-cache"
}
URL = "https://www.goodreads.com/shelf/show/non-fiction"
PAGE_URL_TEXT = "?page="

REPORTS_PATH = "./reports/"

def log_into_goodreads(driver):
  login_url = "https://www.goodreads.com/user/sign_in"
  driver.get(login_url)

  access_sign_in_btn = driver.find_element(By.CLASS_NAME, "authPortalSignInButton")
  access_sign_in_btn.click()
  load_dotenv()
  email_field = driver.find_element(By.ID, "ap_email")
  password_field = driver.find_element(By.ID, "ap_password")
  email_field.send_keys(os.getenv("GR_EMAIL"))
  password_field.send_keys(os.getenv("GR_PASSWORD"))
  sign_in_btn = driver.find_element(By.ID,"signInSubmit")
  sign_in_btn.click()

def selenium_request():
  driver = webdriver.Chrome()
  log_into_goodreads(driver)
  driver.get(URL)
  driver.quit()

def soup_init():
  response = requests.get(URL, headers=HEADERS)
  return BeautifulSoup(response.content, "html.parser")

def scrape_books_in_page(soup):
  books_table = soup.find_all("div", class_="elementList")
  data = []
  for e in books_table:
    title = e.find("a", class_="bookTitle")
    additional_text = e.find("span", class_="greyText smallText")

    if title:
      book = {
        "title": title.text,
        "additional_text": additional_text.text
      }
      data.append(book)
  return data

def extract(soup):
  data = scrape_books_in_page(soup)
  df = pd.DataFrame(data)
  return df

def split_additional_text(row):
  additional_text_sep = "—"
  additional_text = row.additional_text
  additional_text = re.sub(r"\s+", "", additional_text)
  additional_text = additional_text.split(additional_text_sep)

  row['average_rating'] = additional_text[0]
  row['amount_rating'] = additional_text[1]
  row['publishing_year'] = additional_text[2]
  return row

def clean(book_list):
  book_list = book_list.apply(split_additional_text, axis=1)
  book_list = book_list.drop("additional_text", axis=1)

  book_list.average_rating = book_list.average_rating.str.replace(r"[a-zA-Z]", "", regex=True)
  book_list.average_rating = book_list.average_rating.astype("float")
  book_list.amount_rating = book_list.amount_rating.str.replace(r"[a-zA-Z,]", "", regex=True)
  book_list.amount_rating = book_list.amount_rating.astype("int")
  book_list.publishing_year = book_list.publishing_year.str.replace(r"[a-zA-Z]", "", regex=True)
  book_list.publishing_year = book_list.publishing_year.astype("int")

  return book_list

def generate_report(book_list):
  filename = "book_list.csv"
  filepath = REPORTS_PATH + filename
  book_list.to_csv(filepath)
  print(f"See saved report as { filepath }")

def main():
  selenium_request()

  # soup = soup_init()
  # book_list = extract(soup)
  # clean_book_list = clean(book_list)
  # generate_report(clean_book_list)
  # print(clean_book_list.head(5))

if __name__ == '__main__':
  main()