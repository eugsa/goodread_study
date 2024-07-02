import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

URL = "https://www.goodreads.com/shelf/show/non-fiction"

def main():
  page = urlopen(URL)
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")

  soup = BeautifulSoup(html, "html.parser")
  print(soup.title.string)

  r = soup.find_all("a", class_="bookTitle")
  print(r[0].string)

if __name__ == '__main__':
  main()