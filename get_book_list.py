from parser_utils import *
from extract import *
from transform import *
from export import *

def main():
    driver = selenium_request()
    book_list = extract_data(driver)
    clean_book_list = clean(book_list)
    generate_report(clean_book_list)
    driver.quit()

if __name__ == '__main__':
    main()