from parser_utils import *
from extract import *
from transform import *
from export import *

def main():
  driver = selenium_request()
  soup = soup_init(driver.page_source)
  book_list = extract_data(driver, soup)
  clean_book_list = clean(book_list)
  generate_report(clean_book_list)
  print(clean_book_list.head(5))
  driver.quit()

if __name__ == '__main__':
  main()