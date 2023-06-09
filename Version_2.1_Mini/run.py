import subprocess
import webbrowser
import os

# Install required packages from requirements.txt
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])


# Run your first script
subprocess.run(['python', 'ScraperTool_AirBnB.py'])

# Once the first script finishes, run your second script
subprocess.run(['python', 'ScrapeToMap3.py'])