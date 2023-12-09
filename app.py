import pandas as pd
from bs4 import BeautifulSoup

# Read HTML data from a file
with open('moneyball.html', 'r', encoding='utf-8') as file:
    html_data = file.read()

# Parse HTML data
soup = BeautifulSoup(html_data, 'html.parser')

# Extract header and data
header = [th.text.strip() for th in soup.find_all('th')]
data = [[td.text.strip() for td in tr.find_all('td')] for tr in soup.find_all('tr') if tr.find_all('td')]

# Create a DataFrame
df = pd.DataFrame(data, columns=header)

# Define target values
targets = {
    'Good': {'xGP/90': 0.25, 'Con/90': 0.75, 'Int/90': 0.22, 'Pas %': 97},
    'OK': {'xGP/90': 0, 'Con/90': 1.41, 'Int/90': 0.1, 'Pas %': 78},
    'Poor': {'xGP/90': -0.38, 'Con/90': 2.15, 'Int/90': 0.04, 'Pas %': 47},
}

# Create a new column for the overall score
df['Overall Score'] = 0

# Iterate over each player and calculate the score
for index, row in df.iterrows():
    score = 0
    def safe_float_convert(str):
        try:
            return float(str)
        except ValueError:
            return None

    # Then in your loop:
    for stat, target_values in targets.items():
        for column in target_values:
            if column in df.columns:
                target_value = target_values[column]
                player_value = safe_float_convert(row[column].replace('%', ''))
                if player_value is not None:
                    score += abs(target_value - player_value)

    df.at[index, 'Overall Score'] = score

# Define rating thresholds for overall score
good_threshold = 5
ok_threshold = 10

# Create a new column for the overall rating
df['Overall Rating'] = pd.cut(df['Overall Score'], bins=[-float('inf'), good_threshold, ok_threshold, float('inf')], labels=['Good', 'OK', 'Poor'])

# Sort the DataFrame by the Overall Score
df = df.sort_values(by='Overall Score')

# Display the updated DataFrame with Overall Score and Rating
print(df[['Name', 'Overall Score', 'Overall Rating']])
