import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer



def load_data(file_path):
    "loads the ideas CSV into the data frame"
    df = pd.read_csv(file_path)
    print(f"Loaded data with {len(df)} rows.")
    return df






def preprocess_data(df):
    "cleans data for processing"
    df = df.copy()
    df['Description'] = df['Description'].fillna('')
    df['Description'] = df['Description'].str.lower()
    df['Description'] = df['Description'].str.replace(r'[^a-zA-Z\s]', '', regex = True)
    df['Description'] = df['Description'].astype(str)

    print("preprocoessed Dataframe:", df.head())
    return df


    print("Text Data processed")


def vectorize_data(df):
    vectorizer = TfidfVectorizer(stop_words='english')
    print("Vectorizer Object:", vectorizer)

    # Ensure 'Description' column exists and is not empty
    if 'Description' not in df.columns:
        raise ValueError("Column 'Description' not found in DataFrame")

    # Check if DataFrame or column is empty
    if df.empty:
        raise ValueError("The DataFrame is empty")

    if df['Description'].empty:
        raise ValueError("Column 'Description' is empty")

    # Convert column to string
    df['Description'] = df['Description'].astype(str)

    # Print data sample for debugging
    print(df['Description'].head())

    x = vectorizer.fit_transform(df['Description'])


    "Trouble Shoot"
    print("Data has been vectorized")

    return x, vectorizer


