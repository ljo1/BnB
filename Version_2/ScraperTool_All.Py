import csv
import datetime
import pandas as pd
import os
import PySimpleGUI as sg
from apify_client import ApifyClient
from tqdm import tqdm

# Define the GUI layout
layout = [
    [sg.Text('Select Check-in Date')],
    [sg.CalendarButton('Check-in Date', target='check_in_date', format='%Y-%m-%d', key='check_in_date')],
    [sg.Text('Select Check-out Date')],
    [sg.CalendarButton('Check-out Date', target='check_out_date', format='%Y-%m-%d', key='check_out_date')],
    [sg.Button('Submit')]
]

# Create the GUI window
window = sg.Window('Scrapers', layout)

# Event loop to handle GUI events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == 'Submit':
        check_in_date = datetime.datetime.strptime(values['check_in_date'], '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(values['check_out_date'], '%Y-%m-%d')

        # Close the GUI window
        window.close()
        break

# Calculate the total number of days for progress bar
total_days = (check_out_date - check_in_date).days
current_date = check_in_date

# Clear the command screen
os.system('cls' if os.name == 'nt' else 'clear')

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_4BU4ohMtdOk5SfnU7LIwV556YXlRfZ09rV4W")

# Initialize DataFrame to hold all data
all_airbnb_data = pd.DataFrame()
all_booking_data = pd.DataFrame()

# Create a progress bar
pbar = tqdm(total=total_days, ncols=100, desc='Progress')

# Iterate over the dates
while current_date <= check_out_date:
    # Prepare the input for AirBNB scraper
    airbnb_input = {
        "locationQuery": "Corfu, Greece",
        "maxListings": 100,
        "startUrls": [],
        "maxReviews": 0,
        "calendarMonths": 0,
        "currency": "EUR",
        "proxyConfiguration": {"useApifyProxy": True},
        "maxConcurrency": 50,
        "limitPoints": 500,
        "maxPrice": 1000,
        "timeoutMs": 300000,
        "checkIn": current_date.strftime('%Y-%m-%d'),
    }

    # Run the AirBNB scraper and wait for it to finish
    airbnb_run = client.actor("dtrungtin/airbnb-scraper").call(run_input=airbnb_input)

    # Fetch the results from the run's dataset
    airbnb_data = [item for item in client.dataset(airbnb_run["defaultDatasetId"]).iterate_items()]

    # Convert the data to a DataFrame and append it to the all_airbnb_data DataFrame
    all_airbnb_data = pd.concat([all_airbnb_data, pd.DataFrame(airbnb_data)], ignore_index=True)

    # Prepare the input for Booking scraper
    booking_input = {
        "search": "Corfu, Greece",
        "maxPages": 1,
        "sortBy": "distance_from_search",
        "currency": "EUR",
        "language": "en-us",
        "minMaxPrice": "0-700",
        "maxReviews": 0,
        "checkIn": current_date.strftime('%Y-%m-%d'),
        "proxyConfig": {"useApifyProxy": True},
        "extendOutputFunction": "($) => { return {} }",
    }

    # Run the Booking scraper and wait for it to finish
    booking_run = client.actor("dtrungtin/booking-scraper").call(run_input=booking_input)

    # Fetch the results from the run's dataset
    booking_data = [item for item in client.dataset(booking_run["defaultDatasetId"]).iterate_items()]

    # Convert the data to a DataFrame and append it to the all_booking_data DataFrame
    all_booking_data = pd.concat([all_booking_data, pd.DataFrame(booking_data)], ignore_index=True)

    # Increment the current date
    current_date += datetime.timedelta(days=1)

    # Update the progress bar
    pbar.update(1)

# Close the progress bar
pbar.close()

# Write the data to the CSV files
all_airbnb_data.to_csv('airbnb_data.csv', index=False)
all_booking_data.to_csv('booking_data.csv', index=False)
