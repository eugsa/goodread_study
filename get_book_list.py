import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

URL = "https://www.goodreads.com/shelf/show/non-fiction"

def soup_init():
  page = urlopen(URL)
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")
  return BeautifulSoup(html, "html.parser")

def extract(soup):
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
  return book_list

def main():
  soup = soup_init()
  book_list = extract(soup)
  clean_book_list = clean(book_list)
  print(clean_book_list.sample(n=20))

if __name__ == '__main__':
  main()