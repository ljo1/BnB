import csv
import datetime
import pandas as pd
import os
from apify_client import ApifyClient
from tqdm import tqdm

# Clear the command screen
os.system('cls' if os.name == 'nt' else 'clear')

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_4BU4ohMtdOk5SfnU7LIwV556YXlRfZ09rV4W")

current_date = datetime.datetime.today().strftime('%Y-%m-%d')

# Prepare initial actor input
run_input = {
    "locationQuery": "Corfu, Greece",
    "maxListings": 40,
    "startUrls": [],
    "maxReviews": 0,
    "calendarMonths": 0,
    "currency": "EUR",
    "proxyConfiguration": {"useApifyProxy": True},
    "maxConcurrency": 100,
    "limitPoints": 500,
    "maxPrice" : 1000,
    "timeoutMs": 300000,
    "checkIn": current_date,
}

# Initialize DataFrame to hold all data
all_data = pd.DataFrame()

# Check if the CSV file already exists, if so load its data
if os.path.isfile('airbnb_data.csv'):
    all_data = pd.read_csv('airbnb_data.csv')

# Define your check-in and check-out dates
check_in_date = datetime.datetime.today()
check_out_date = check_in_date + datetime.timedelta(days=7)

# Calculate the total days
total_days = (check_out_date - check_in_date).days

# Create a progress bar
pbar = tqdm(total=total_days, ncols=100, desc='Progress')

# Iterate over the dates
current_date = check_in_date
while current_date <= check_out_date:
    # Update the check-in date in the actor input
    run_input['checkIn'] = current_date.strftime('%Y-%m-%d')

    # Run the actor and wait for it to finish
    run = client.actor("dtrungtin/airbnb-scraper").call(run_input=run_input)

    # Fetch the results from the run's dataset
    data = [item for item in client.dataset(run["defaultDatasetId"]).iterate_items()]

    # Convert the data to a DataFrame and append it to the all_data DataFrame
    all_data = pd.concat([all_data, pd.DataFrame(data)], ignore_index=True)

    # Increment the current date
    current_date += datetime.timedelta(days=1)

    # Update the progress bar
    pbar.update(1)

# Close the progress bar
pbar.close()

# Write the data to the CSV file
all_data.to_csv('airbnb_data.csv', mode='a', header= not os.path.isfile('airbnb_data.csv'), index=False)
