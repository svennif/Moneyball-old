import pandas as pd
from bs4 import BeautifulSoup
from IPython.display import display

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
    "Good": {"xGP/90": 0.25, "Con/90": 0.75, "Int/90": 0.22, "Pas %": 97},
    "OK": {"xGP/90": 0, "Con/90": 1.41, "Int/90": 0.1, "Pas %": 78},
    "Poor": {"xGP/90": -0.38, "Con/90": 2.15, "Int/90": 0.04, "Pas %": 47},
}

# Remove any non-numeric characters
df['Pas %'] = df['Pas %'].str.replace('%', '', regex=False)

# Convert the column to integer
df['Pas %'] = df['Pas %'].astype(int)

def color_based_on_value(row):
    colors = []
    for val, name in zip(row, row.index):
        if val >= targets['Good'][name]:
            colors.append('color: green')
        elif val >= targets['OK'][name]:
            colors.append('color: orange')
        else:
            colors.append('color: red')
    return colors

# Convert the selected columns to numeric and round to 2 decimal places
for col in ["xGP/90", "Con/90", "Int/90", "Pas %"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    if col != "Pas %":  # We don't want to round "Pas %" as it's converted to int
        df[col] = df[col].round(2)

# Now apply the color_based_on_value function only to selected columns
styled_df = df.style.apply(color_based_on_value, subset=headers, axis=1)

# Render to HTML
html = styled_df._repr_html_()

with open('styled_dataframe.html', 'w', encoding='utf-8') as f:
    f.write(html)