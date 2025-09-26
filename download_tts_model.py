import os
import logging

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the local directory where you want to save the model
local_dir = "./downloaded_model"  # Replace with your desired path

# Create the directory if it doesn't exist
os.makedirs(local_dir, exist_ok=True)

logging.info(f"Downloading files to '{local_dir}'...")

# Correct the git clone command to execute within the script
os.system(f"git clone https://huggingface.co/coqui/XTTS-v2 {local_dir}")

logging.info(f"Files downloaded successfully to: {local_dir}")