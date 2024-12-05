import logging
import requests
import pandas as pd
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


def call_data(api_key: str, base_url: str, endpoint: str) -> Optional[pd.DataFrame]:
    """
    Fetch paginated data from the API and return it as a Pandas DataFrame.

    Args:
        api_key (str): API key for authorization.
        base_url (str): Base URL of the API.
        endpoint (str): Endpoint for the specific data resource.

    Returns:
        DataFrame: A Pandas DataFrame containing the fetched data, or None if an error occurs.
    """
    try:
        # Build the complete URL
        ideas_url = f"{base_url}/{endpoint}"
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }

        # Initialize an empty list to collect data from all pages
        all_ideas = []

        # Start by setting the current page to 1
        current_page = 1

        # Fetch data while the current page is less than or equal to the total number of pages
        while True:
            # Append the current page number to the URL
            paginated_url = f"{ideas_url}?page={current_page}"

            # Make the request
            response = requests.get(paginated_url, headers=headers)

            if response.status_code == 200:
                data = response.json()  # Convert response to JSON

                # Extract the total number of pages from the first response
                if current_page == 1:
                    total_pages = data['pagination'][0].get('total_pages', 1)
                    logging.info(f"Total pages to fetch: {total_pages}")

                # Extract the rows part of the JSON which contains the actual data
                rows_data = data.get('rows', [])

                # Convert rows into a flat structure for each idea
                for row in rows_data:
                    idea = {
                        'Idea Reference': row[0].get('plain_value', ''),
                        'Name': row[1].get('plain_value', ''),
                        'Categories': row[2].get('plain_value', ''),
                        'Assigned_to': row[3].get('plain_value', ''),
                        'Status': row[4].get('plain_value', ''),
                        'Created_at': row[5].get('plain_value', ''),
                        'Votes': row[6].get('plain_value', ''),
                        'Tags': row[7].get('plain_value', ''),
                        'Description': row[8].get('plain_value', ''),
                        'Idea ID': row[9].get('plain_value', ''),
                        'Email': row[10].get('plain_value', ''),
                    }
                    all_ideas.append(idea)

                # Increment to the next page
                current_page += 1

                # Break the loop if we've reached the last page
                if current_page > total_pages:
                    break
            else:
                logging.error(f"API request failed: {response.status_code} - {response.text}")
                break

        # Convert the collected data into a DataFrame
        df = pd.DataFrame(all_ideas)
        logging.info(f"Fetched {len(df)} records from the API")
        return df

    except requests.exceptions.RequestException as e:
        logging.error(f"Error making API request: {e}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return None


api_key = os.getenv('API_KEY')
base_url = 'https://cpsideas.aha.io/api/v1/bookmarks/custom_pivots'
endpoint = '/7433888668818238535'

df = call_data(api_key, base_url, endpoint)

if df is not None:
    print(df.head())
else:
    print("error fetching data")
