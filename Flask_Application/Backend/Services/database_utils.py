import os
import pandas as pd
from sqlalchemy import create_engine

def save_to_database(df: pd.DataFrame, db_filename: str = 'test_database.sqlite', table_name: str = 'Idea_Database'):
    """
    Save the DataFrame to an SQLite database.

    Args:
        df (pd.DataFrame): The DataFrame to save.
        db_filename (str): The name of the SQLite database file.
        table_name (str): The name of the table in the database where the DataFrame will be stored.

    Returns:
        None
    """
    try:
        # Get the path for the database file
        db_path = os.path.join(os.getcwd(), db_filename)

        # Log the resolved database path
        print(f"Resolved database path: {db_path}")

        # Create an SQLAlchemy engine to connect to the SQLite file
        engine = create_engine(f'sqlite:///{db_path}', echo=False)

        # Log the details about the save operation
        print(f"Saving data to table '{table_name}' in database: {db_path}")

        # Save the DataFrame to the SQLite database (replace table if exists)
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)  # Save without the index column

        print(f"Data successfully saved to SQLite database at: {db_path}")
    except Exception as e:
        print(f"Error saving DataFrame to SQL: {e}")

if __name__ == "__main__":
    # Create a sample DataFrame for debugging
    data = {
        "Topic": [1, 2, 3],
        "Description": ["Topic 1 description", "Topic 2 description", "Topic 3 description"],
        "ID": [101, 102, 103],
    }
    df = pd.DataFrame(data)

    # Log the DataFrame contents
    print("DataFrame to be saved:")
    print(df)

    # Call the save_to_database function with the sample DataFrame
    save_to_database(df)
