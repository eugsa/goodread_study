import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

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

    if title is not None:
      book = {
        "title": title.text,
        "additional_text": additional_text.text
      }
      data.append(book)

  df = pd.DataFrame(data)
  print(df.sample(n=20))
  return df

def main():
  soup = soup_init()
  book_list = extract(soup)

if __name__ == '__main__':
  main()