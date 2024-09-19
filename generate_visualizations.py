import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import config

def tag_ranking(dnf_df, nonfic_in_dnf):
    new_df = nonfic_in_dnf[[ "title"]]
    result_df = new_df.copy()
    result_df["nonfic_ranking"] = result_df.index
    dnf_df_reset = dnf_df.reset_index()
    result_df = result_df.merge(dnf_df_reset[['title', 'index']], on='title', how='left')
    result_df.rename(columns={'index': 'dnf_ranking'}, inplace=True)
    
    sns.set_theme(style="whitegrid")
    sns.scatterplot(data=result_df, x="dnf_ranking", y="nonfic_ranking")
    plt.show()

def books_in_dnf(nonfic_df, nonfic_in_dnf):
    count = {
        "count_nonfic_total": len(nonfic_df),
        "count_nonfic_in_dnf": len(nonfic_in_dnf)
    }

    sns.set_theme(style="whitegrid", palette="Set2")
    sns.catplot(data=count, kind="bar")
    plt.show()

def visualize_data(nonfic_books_csv, dnf_books_csv):
    nonfic_df = pd.read_csv(nonfic_books_csv, index_col=0)
    dnf_df = pd.read_csv(dnf_books_csv, index_col=0)
    nonfic_in_dnf = nonfic_df[nonfic_df.title.isin(dnf_df.title)]

    books_in_dnf(nonfic_df, nonfic_in_dnf)
    tag_ranking(dnf_df, nonfic_in_dnf)

def main():
    nonfic_books_csv = config.REPORTS_PATH + config.NONFIC_FILENAME
    dnf_books_csv = config.REPORTS_PATH + config.DNF_FILENAME

    if os.path.isfile(nonfic_books_csv) and os.path.isfile(dnf_books_csv):
        visualize_data(nonfic_books_csv, dnf_books_csv)
    else:
        print("""
              Please first scrape the data for non-fiction and dnf books
              with the get_book_data.py script.
        """)

if __name__ == '__main__':
    main()
