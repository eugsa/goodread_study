import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

URL = "https://www.goodreads.com/shelf/show/non-fiction"

def main():
  page = urlopen(URL)
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")

  title_index = html.find("<title>")
  start_title_index = title_index + len("<title>")
  end_title_index = html.find("</title>")
  title = html[start_title_index:end_title_index]
  print(title)

if __name__ == '__main__':
  main()