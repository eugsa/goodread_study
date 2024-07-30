"""Main method conducting the whole ETL process."""
import parser_utils
import extract
import transform
import export

def main():
    driver = parser_utils.selenium_request()
    book_list = extract.extract_data(driver)
    clean_book_list = transform.clean(book_list)
    export.generate_report(clean_book_list)
    driver.quit()

if __name__ == '__main__':
    main()
