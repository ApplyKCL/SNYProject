#!/bin/bash

# Install dependencies from requirements.txt file using pip
cd Working_Process_Tracker
pip install -r requirements.txt
echo "Dependencies installation complete."

# Create the database
cd db_program
echo "---------------------------------------------"
echo "Follow the instuctions to create the database"
python admin_console.py
echo "Database creation complete."
cd ../