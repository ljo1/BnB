import subprocess
import webbrowser
import os


# Run your first script
subprocess.run(['python3', 'ScrapeTool1.py'])

# Once the first script finishes, run your second script
subprocess.run(['python3', 'ScrapeToMap2.py'])

# Assuming your HTML file is 'heatmap.html' and it's in the same directory
file_path = os.path.abspath('heatmap.html')

# Open the file in the default web browser
webbrowser.open('file://' + file_path)