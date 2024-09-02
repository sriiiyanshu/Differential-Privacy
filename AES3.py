from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import pandas as pd
import json
import os

# Function to encrypt data using AES
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    return cipher.nonce, tag, ciphertext

# Function to decrypt data using AES
def decrypt_data(nonce, tag, ciphertext, key):
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    data = cipher.decrypt_and_verify(ciphertext, tag)
    return data.decode('utf-8')

# Function to generate and save AES key to a file
def generate_and_save_key(filename):
    key = get_random_bytes(32)
    with open(filename, 'wb') as f:
        f.write(key)
    return key

# Function to read AES key from a file
def read_key(filename):
    with open(filename, 'rb') as f:
        key = f.read()
    return key

# Generate or read AES key from file
key_filename = 'aes_key.bin'
if not os.path.exists(key_filename):
    key = generate_and_save_key(key_filename)
else:
    key = read_key(key_filename)

# Load dataset
dataset = pd.read_csv('healthcare_dataset.csv')

# Convert DataFrame to JSON string
data_json = dataset.to_json()

# Encrypt the data
nonce, tag, ciphertext = encrypt_data(data_json, key)

# Save the encrypted data to a file
with open('encrypted_data.json', 'wb') as f:
    f.write(nonce)
    f.write(tag)
    f.write(ciphertext)

# Read the encrypted data from the file
with open('encrypted_data.json', 'rb') as f:
    nonce = f.read(16)
    tag = f.read(16)
    ciphertext = f.read()

# Decrypt the data
decrypted_data = decrypt_data(nonce, tag, ciphertext, key)

# Convert decrypted data from JSON to DataFrame
decrypted_df = pd.read_json(decrypted_data)

# Save decrypted data to a new CSV file
decrypted_df.to_csv('decrypted_dataset.csv', index=False)
