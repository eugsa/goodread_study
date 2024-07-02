import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup

URL = "https://www.goodreads.com/shelf/show/non-fiction"

def main():
  # dfs = pd.read_html(URL)
  # print(dfs)

  page = urlopen(URL)
  html_bytes = page.read()
  html = html_bytes.decode("utf-8")

  soup = BeautifulSoup(html, "html.parser")
  print(soup.title.string)

  table = soup.find_all("a", class_="bookTitle")
  data = []
  for e in table:
    title = e.get_text(strip=True)
    data.append({"title": title})

  df = pd.DataFrame(data)
  print(df.sample(n=20))

if __name__ == '__main__':
  main()