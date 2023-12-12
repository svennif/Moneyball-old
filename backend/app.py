from flask import Flask
import pandas as pd
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()

# Read HTML data from a file
with open("moneyball.html", "r", encoding="utf-8") as file:
    html_data = file.read()

# Parse HTML data
soup = BeautifulSoup(html_data, "lxml")

# Extract header and data
header = [th.text.strip() for th in soup.find_all("th")]
data = [
    [td.text.strip() for td in tr.find_all("td")]
    for tr in soup.find_all("tr")
    if tr.find_all("td")
]

# Create a DataFrame
df = pd.DataFrame(data, columns=header)

# Select the follwing headers
headers = ["xGP/90", "Con/90", "Int/90", "Pas %"]

# Define target values
targets = {
    "Good": {"xGP/90": 0.25, "Con/90": 0.75, "Int/90": 0.22, "Pas %": 93},
    "OK": {"xGP/90": 0, "Con/90": 1.41, "Int/90": 0.1, "Pas %": 78},
    "Poor": {"xGP/90": -0.38, "Con/90": 2.15, "Int/90": 0.04, "Pas %": 47},
}

# Remove any non-numeric characters
df["Pas %"] = df["Pas %"].str.replace("%", "", regex=False)

# Convert the column to integer
df["Pas %"] = pd.to_numeric(df["Pas %"], errors="coerce").astype(int)

# Convert the selected columns to numeric and round to 2 decimal places
for col in ["xGP/90", "Con/90", "Int/90"]:
    df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
    df[col] = df[col].fillna("-")

print(df)
