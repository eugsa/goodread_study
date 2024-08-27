"""Provides methods cleaning and transforming the data."""
import re
import math

def split_additional_text(row):
    additional_text_sep = "—"
    additional_text = row.additional_text
    additional_text = re.sub(r"\s+", "", additional_text)
    additional_text = additional_text.split(additional_text_sep)

    row['average_rating'] = additional_text[0]
    row['amount_rating'] = additional_text[1]
    row['publishing_year'] = additional_text[2]
    return row

def metric_char_conversion(currently_reading_count):
    if (not currently_reading_count
        or (isinstance(currently_reading_count, float) and math.isnan(currently_reading_count))):
        return currently_reading_count
    elif "k" in currently_reading_count:
        return float(currently_reading_count.replace("k", "")) * 10**3
    elif "m" in currently_reading_count:
        return float(currently_reading_count.replace("m", "")) * 10**6
    return float(currently_reading_count)

def clean(book_list):
    book_list = book_list.apply(split_additional_text, axis=1)
    book_list = book_list.drop("additional_text", axis=1)

    book_list.average_rating = book_list.average_rating.str.replace(r"[a-zA-Z]", "", regex=True)
    book_list.average_rating = book_list.average_rating.astype("float", errors='ignore')
    book_list.amount_rating = book_list.amount_rating.str.replace(r"[a-zA-Z,]", "", regex=True)
    book_list.amount_rating = book_list.amount_rating.astype("int", errors='ignore')
    book_list.publishing_year = book_list.publishing_year.str.replace(r"[a-zA-Z]", "", regex=True)
    book_list.publishing_year = book_list.publishing_year.astype("int", errors='ignore')
    book_list.page_count = book_list.page_count.str.split().str[0]
    book_list.page_count = book_list.page_count.astype("int", errors='ignore')
    book_list.price = book_list.price.str.split().str[1].str.replace('$', '')
    book_list.price = book_list.price.astype("float", errors='ignore')
    book_list.currently_reading_count = book_list.currently_reading_count.str.split().str[0].str.replace(',', '')
    book_list.currently_reading_count = book_list.currently_reading_count.apply(metric_char_conversion)
    book_list.wanting_to_read_count = book_list.wanting_to_read_count.str.split().str[0].str.replace(',', '')
    book_list.wanting_to_read_count = book_list.wanting_to_read_count.apply(metric_char_conversion)

    return book_list
