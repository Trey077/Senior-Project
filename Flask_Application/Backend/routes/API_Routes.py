import logging

import requests
import pandas as pd
import json
from dotenv import load_dotenv
import os


load_dotenv()

API_KEY = os.getenv("API_KEY")


def call_data(api_key, base_url, endpoint):


    url = 'https://cpsideas.aha.io/api/v1/bookmarks/custom_pivots'
    ideas_url = f'{url}/7433888668818238535'

    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    # Initialize an empty list to collect data from all pages
    all_ideas = []

    # Start by setting the current page to 1
    current_page = 1

    # Fetch data while the current page is less than or equal to the total number of pages
    while True:
        # Append the current page number to the URL
        paginated_url = f'{ideas_url}?page={current_page}'

        # Make the request
        response = requests.get(paginated_url, headers=headers)

        if response.status_code == 200:
            data = response.json()  # Convert response to JSON

            # Extract the total number of pages from the first response
            if current_page == 1:
                total_pages = data['pagination'][0]['total_pages']
                print(f"Total pages: {total_pages}")

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
            print(f"Error: {response.status_code} - {response.text}")
            break

    df = pd.DataFrame(all_ideas)
    logging.info(f"Fetched {len(df)} records from the API")
    return df


call_data()






