import logging

from Flask_Application.Backend.Services.api_call import call_data
from Flask_Application.Backend.Services.top2vec_model import generate_topic_dataframe
from Flask_Application.Backend.Services.dataframe_merge import merge_dataframes
from Flask_Application.Backend.Services.database_utils import save_to_database
import pandas as pd




def process_and_store(api_key, base_url, endpoint,num_topics, topic_docs, model_path, merge_column,  db_path, table_name):
    """
    Full pipeline: fetch API data, process topics, merge data, and save to DB.

    Args:
        api_key (str): API key for the API.
        base_url (str): Base URL of the API.
        endpoint (str): API endpoint.
        model_path (str): Path to the Top2Vec model.
        db_path (str): Path to the SQLite database.
        table_name (str): Name of the database table.
        merge_column (str): Column in the DataFrame containing text data.
    """
    try:
        # Step 1: Fetch API Data
        logging.info("Fetching API data...")
        ideas_df = call_data(api_key, base_url, endpoint)
        if ideas_df.empty:
            logging.warning("No data fetched from the API.")
            return


        # Step 2: Generate Topic Data and create DF
        logging.info("Extracting topics from the model...")
        topics_df = generate_topic_dataframe(model_path, num_topics , topic_docs)

        # Step 3: Merge DF
        logging.info("Merging the dataframes...")
        combined_df = merge_dataframes(ideas_df, topics_df, merge_column)


        # Step 4: Save Combined Data to Database
        logging.info("Saving combined data to the database...")
        if save_to_database(combined_df, db_path, table_name):
            logging.info("Data successfully saved to the database.")
        else:
            logging.error("Failed to save data to the database.")

    except Exception as e:
        logging.error(f"Error in the data processing pipeline: {e}")
