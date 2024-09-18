"""Provides methods to export the data."""
import config

def generate_report(shelf, book_list):
    filepath = config.REPORTS_PATH + shelf + config.BOOKS_END_FILENAME
    book_list.to_csv(filepath)
    print(f"See saved report as { filepath }")
