import csv
import json
import os

import requests
from dotenv import load_dotenv

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
API_KEY = os.getenv("API_KEY")

# -----------------------------
# Read employees.csv
# -----------------------------
employees = []

with open("employees.csv", "r", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        employees.append(row)

# Write employees.json
with open("employees.json", "w", encoding="utf-8") as file:
    json.dump(employees, file, indent=4)

# High earners
high_earners = [
    employee
    for employee in employees
    if float(employee["salary"]) > 50000
]

# Write high_earners.csv
with open("high_earners.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["id", "name", "department", "salary", "city"]
    )

    writer.writeheader()
    writer.writerows(high_earners)

print(f"Rows read: {len(employees)} | High earners: {len(high_earners)}")

# -----------------------------
# API Call
# -----------------------------
BASE_URL = "https://jsonplaceholder.typicode.com"

try:
    response = requests.get(f"{BASE_URL}/users", timeout=5)
    response.raise_for_status()

    users = response.json()

    # Print first 3 users
    for user in users[:3]:
        print(f'{user.get("id")} - {user.get("name")} - {user.get("email")}')

    # Extract nested JSON safely
    simplified_users = []

    for user in users:
        simplified_users.append({
            "id": user.get("id"),
            "name": user.get("name"),
            "email": user.get("email"),
            "city": user.get("address", {}).get("city"),
            "company": user.get("company", {}).get("name")
        })

    with open("users.json", "w", encoding="utf-8") as file:
        json.dump(simplified_users, file, indent=4)

except requests.exceptions.Timeout:
    print("Timeout occurred.")

except requests.exceptions.ConnectionError:
    print("Connection error.")

except requests.exceptions.RequestException as error:
    print(error)

# -----------------------------
# 404 Example
# -----------------------------
try:
    response = requests.get(f"{BASE_URL}/users/9999", timeout=5)

    if response.status_code == 404:
        print("/users/9999 -> 404 Not found")

except requests.exceptions.Timeout:
    print("Timeout while checking user.")