"""Provides methods to export the data."""
import config

def generate_report(book_list):
    filename = "book_list.csv"
    filepath = config.REPORTS_PATH + filename
    book_list.to_csv(filepath)
    print(f"See saved report as { filepath }")
