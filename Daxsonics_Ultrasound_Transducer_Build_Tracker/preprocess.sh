#!/bin/bash

# Install dependencies from requirements.txt file using pip
pip install -r requirements.txt

echo "Dependencies installation complete."

cd db_program
python admin_console.py

echo "Database creation complete."

cd ../