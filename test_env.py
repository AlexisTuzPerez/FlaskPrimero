#!/usr/bin/env python3
import os
from dotenv import load_dotenv

print("Before loading .env:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")

print("\nLoading .env file...")
load_dotenv()

print("\nAfter loading .env:")
print(f"DB_HOST: {os.getenv('DB_HOST')}")
print(f"DB_USER: {os.getenv('DB_USER')}")
print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
print(f"DB_NAME: {os.getenv('DB_NAME')}")
print(f"DB_PORT: {os.getenv('DB_PORT')}")

# Check if .env file exists and read its contents
env_path = '.env'
if os.path.exists(env_path):
    print(f"\n.env file exists at: {os.path.abspath(env_path)}")
    with open(env_path, 'r') as f:
        content = f.read()
        print(f"Content of .env file:")
        print(repr(content))
else:
    print(f"\n.env file not found at: {os.path.abspath(env_path)}")
