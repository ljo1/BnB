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
window = sg.Window('Booking Scraper', layout)

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
    "search": "Corfu, Greece",
    "maxPages": 2,
    "sortBy": "distance_from_search",
    "currency": "EUR",
    "language": "en-us",
    "minMaxPrice": "0-1000",
    "maxReviews": 0,
    "checkIn": current_date,
    "proxyConfig": { "useApifyProxy": True },
    "extendOutputFunction": "($) => { return {} }"
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
    run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

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
all_data.to_csv('booking_data.csv', index=False)
