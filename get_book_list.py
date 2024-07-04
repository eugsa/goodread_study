import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

URL = "https://www.goodreads.com/shelf/show/non-fiction"
REPORTS_PATH = "./reports/"

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
  soup = soup_init()
  book_list = extract(soup)
  clean_book_list = clean(book_list)
  generate_report(clean_book_list)
  print(clean_book_list.head(50))
  print(clean_book_list.info())

if __name__ == '__main__':
  main()