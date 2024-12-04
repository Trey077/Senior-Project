import pandas as pd
import top2vec
import sys

from Flask_Application.Backend.routes.API_Routes import call_data


def data_processing():
    df = pd.DataFrame(call_data())

    Documents = df['Description'].tolist()

    while ('' in Documents):
        Documents.remove('')

    return Documents, df


print(data_processing())


#def merge_df():













#Through API data in DF to clean and sort






