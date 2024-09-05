"""Provides methods to export the data."""
import config

def generate_report(book_list):
    filepath = config.REPORTS_PATH + config.BOOKS_FILENAME
    book_list.to_csv(filepath)
    print(f"See saved report as { filepath }")
