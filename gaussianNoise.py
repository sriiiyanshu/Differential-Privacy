import pandas as pd
import numpy as np
import random 
from datetime import datetime, timedelta

# Parameters for Gaussian noise
mean = 0  # Mean of the Gaussian distribution
std_dev = random.randint(5,25)  # Standard deviation of the Gaussian distribution

# Load dataset from CSV file
dataset = pd.read_csv('healthcare_dataset.csv')

# List of columns to exclude from noise addition
exclude_columns = ['Gender', 'Blood Type', 'Medical Condition', 'Medication', 'Test Results']  # Exclude specified columns

# Function to add Gaussian noise to ASCII values
def add_noise_to_ascii(val, mean, std_dev):
    if isinstance(val, str):
        ascii_values = [ord(char) for char in val]
        noisy_ascii_values = []
        for value in ascii_values:
            noisy_value = int(np.round(value + np.random.normal(mean, std_dev)))
            if 65 <= noisy_value <= 90 or 97 <= noisy_value <= 122 or 48 <= noisy_value <= 57:
                noisy_ascii_values.append(noisy_value)
            else:
                noisy_ascii_values.append(value)  # Keep non-alphanumeric characters unchanged
        noisy_string = ''.join([chr(value) for value in noisy_ascii_values])
        return noisy_string
    return val

# Function to add Gaussian noise to Age column while keeping it between 0 and 100
def add_noise_to_age(val, mean, std_dev):
    noisy_val = int(np.round(val + np.random.normal(mean, std_dev)))
    return max(0, min(noisy_val, 100))  # Ensure age remains between 0 and 100

def add_noise_to_room(val, mean, std_dev):
    noisy_val = int(np.round(val + np.random.normal(mean, std_dev)))
    return noisy_val


# Function to add Gaussian noise to Billing Amount column while keeping it positive integer
def add_noise_to_billing_amount(val, mean, std_dev):
    std_dev = random.randint(1000,50000)
    noisy_val = int(np.round(val + np.random.normal(mean, std_dev)))
    return max(0, noisy_val)  # Ensure billing amount remains positive

# Apply the function to the entire DataFrame, excluding certain columns
for col in dataset.columns:
    if col not in exclude_columns:
        if col == 'Age':
            dataset[col] = dataset[col].apply(add_noise_to_age, args=(mean, std_dev))
        elif col == 'Billing Amount':
            dataset[col] = dataset[col].apply(add_noise_to_billing_amount, args=(mean, std_dev))
        elif col=="Room Number":
            dataset[col] = dataset[col].apply(add_noise_to_room , args = (mean, std_dev))
        else:
            dataset[col] = dataset[col].apply(add_noise_to_ascii, args=(mean, std_dev))

# Modify the 'Date of Admission' and 'Discharge Date' columns to have different dates
date_format = "%Y-%m-%d"  # Assuming the date format in the dataset is YYYY-MM-DD
start_date = datetime.strptime('2000-01-01', date_format)  # Start date for generating random dates
end_date = datetime.strptime('2040-12-31', date_format)  # End date for generating random dates

# Function to generate a random date within the specified range
def generate_random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))

dataset['Date of Admission'] = dataset['Date of Admission'].apply(lambda x: generate_random_date(start_date, end_date).strftime(date_format))
dataset['Discharge Date'] = dataset['Discharge Date'].apply(lambda x: generate_random_date(start_date, end_date).strftime(date_format))

# Save the modified dataset to a CSV file
dataset.to_csv('gaussian_noise.csv', index=False)