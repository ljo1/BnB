import csv
import datetime
import pandas as pd
import os
import PySimpleGUI as sg
from apify_client import ApifyClient
from tqdm import tqdm

# Define the GUI layout
layout = [
    [sg.CalendarButton('Select Check-in Date', target='check_in_date', format='%Y-%m-%d')],
    [sg.Input(key='check_in_date', enable_events=True, readonly=True)],
    [sg.CalendarButton('Select Check-out Date', target='check_out_date', format='%Y-%m-%d')],
    [sg.Input(key='check_out_date', enable_events=True, readonly=True)],
    [sg.Button('Submit')]
]

# Create the GUI window
window = sg.Window('AirBNB Scraper', layout)

# Event loop to handle GUI events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Submit':
        check_in_date = datetime.datetime.strptime(values['check_in_date'], '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(values['check_out_date'], '%Y-%m-%d')
        break

# Close the GUI window
window.close()

# Calculate the total number of days for progress bar
total_days = (check_out_date - check_in_date).days
current_date = check_in_date

# Clear the command screen
os.system('cls' if os.name == 'nt' else 'clear')

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_4BU4ohMtdOk5SfnU7LIwV556YXlRfZ09rV4W")

# Prepare initial actor input
run_input = {
    "locationQuery": "Corfu, Greece",
    "maxListings": 25,
    "startUrls": [],
    "maxReviews": 0,
    "calendarMonths": 0,
    "currency": "EUR",
    "proxyConfiguration": {"useApifyProxy": True},
    "maxConcurrency": 50,
    "limitPoints": 500,
    "maxPrice" : 1000,
    "timeoutMs": 300000,
    "checkIn": current_date,
}

# Initialize DataFrame to hold all data
all_data = pd.DataFrame()

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
all_data.to_csv('airbnb_data.csv', index=False)
