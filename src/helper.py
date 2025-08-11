import pandas as pd


def get_keywords(path):
    df = pd.read_excel(path)
    df = df.fillna("")
    keywords = [name for name in df["Commodity Name (consumable)"] if name]
    keywords += [name for name in df["Industry Name (consumable)"] if name]
    keywords = list(set(keywords))
    return keywords