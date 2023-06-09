import subprocess
import webbrowser
import os

# Install required packages from requirements.txt
subprocess.check_call(["pip3", "install", "-r", "requirements.txt"])


# Run your first script
subprocess.run(['python3', 'ScraperTool_All.py'])

# Once the first script finishes, run your second script
subprocess.run(['python3', 'ScrapeToMap3.py'])

# Assuming your HTML file is 'heatmap.html' and it's in the same directory
file_path = os.path.abspath('heatmap.html')

# Open the file in the default web browser
webbrowser.open('file://' + file_path)