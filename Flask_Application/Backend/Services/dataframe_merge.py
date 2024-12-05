import pandas as pd
from Flask_Application.Backend.Services.api_call import call_data
from Flask_Application.Backend.Services.top2vec_model import generate_topic_dataframe
import os
from dotenv import load_dotenv

load_dotenv()




def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, merge_column: str) -> pd.DataFrame:
    """
    Merges two DataFrames based on a common column.

    Args:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.
        merge_column (str): The name of the column to merge the DataFrames on.

    Returns:
        pd.DataFrame: The merged DataFrame.
    """
    try:
        # Merge the two DataFrames on the specified column
        merged_df = pd.merge(df1, df2, on=merge_column, how='inner')  # 'inner' join by default, can change to 'left', 'right', or 'outer'
        print(f"Successfully merged DataFrames on '{merge_column}'.")
        return merged_df

    except KeyError:
        print(f"Error: The column '{merge_column}' does not exist in one or both DataFrames.")
        return pd.DataFrame()  # Return an empty DataFrame if the merge column is not found

    except Exception as e:
        print(f"Unexpected error during merge: {e}")
        return pd.DataFrame()  # Return an empty DataFrame in case of any other error


api_key = os.getenv('API_KEY')
base_url = 'https://cpsideas.aha.io/api/v1/bookmarks/custom_pivots'
endpoint = '/7433888668818238535'
df1 = call_data(api_key, base_url, endpoint)


model_path = "Backend/models/Topic-Model"
df2 = generate_topic_dataframe(model_path,num_topics=13, topic_docs=[451, 210, 180, 163, 157, 137, 136, 120, 116, 112, 104, 92, 92])

merge_column = "Description"

merged_df = merge_dataframes(df1, df2, merge_column)

print(merged_df)


