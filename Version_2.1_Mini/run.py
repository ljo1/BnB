import subprocess
import webbrowser
import os

# Install required packages from requirements.txt
subprocess.check_call(["pip", "install", "-r", "requirements.txt"])


# Run your first script
subprocess.call(['python', 'ScrapeTool_AirBnB.py'])

# Once the first script finishes, run your second script
subprocess.call(['python', 'ScrapeToMap3.py'])