import os
import inspect
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import config

def get_filepath(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, config.FIGURES_PATH + filename)
    return filepath

def saving_figure(plt, filename):
    filepath = get_filepath(filename)
    plt.savefig(filepath)
    print(f"See saved figure as { filepath }.png")
    plt.close()

def tag_ranking(dnf_df, nonfic_in_dnf):
    new_df = nonfic_in_dnf[[ "title"]]
    result_df = new_df.copy()
    result_df["nonfic_ranking"] = result_df.index
    dnf_df_reset = dnf_df.reset_index()
    result_df = result_df.merge(dnf_df_reset[['title', 'index']], on='title', how='left')
    result_df.rename(columns={'index': 'dnf_ranking'}, inplace=True)

    sns.set_theme(style="whitegrid")
    sns.scatterplot(data=result_df, x="dnf_ranking", y="nonfic_ranking")

    filename = inspect.stack()[0][3]
    saving_figure(plt, filename)

def books_in_dnf(nonfic_df, nonfic_in_dnf):
    count = {
        "count_nonfic_total": len(nonfic_df),
        "count_nonfic_in_dnf": len(nonfic_in_dnf)
    }

    sns.set_theme(style="whitegrid", palette="Set2")
    sns.catplot(data=count, kind="bar")

    filename = inspect.stack()[0][3]
    saving_figure(plt, filename)

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
