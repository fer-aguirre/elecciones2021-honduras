import pandas as pd
import numpy as np
import re
import datetime
#!/usr/bin/python3 -m pip install configparser
import configparser
#!/usr/bin/python3 -m pip install botometer
import botometer

# Get API and Oauth keys
parser = configparser.ConfigParser()
parser.read("config.ini")
parser.sections()
rapidapi_key = parser.get('api', 'rapidapi')
parser.options('oauth keys')
consumer_key = parser.get('oauth keys', 'consumer_key')
consumer_secret = parser.get('oauth keys', 'consumer_secret')
access_key = parser.get('oauth keys', 'access_key')
access_secret = parser.get('oauth keys', 'access_secret')

# Read 'csv' file as dataframe
df = pd.read_csv("output/SeVan.csv", index_col=None)

# Create a list with usernames posting the hashtag
usernames = list(df['Username'])

# Remove duplicates usernames
usernames = [i for n, i in enumerate(usernames) if i not in usernames[:n]]
len(usernames)

# Filter usernames with a serie of numbers at the end (at least 5)
usernames_filtered = list(map(lambda x: x[0], filter(None, map(lambda x: re.findall(r'(^.*\d{5})', x), usernames))))
len(usernames_filtered)
usernames_filtered

# Create a column with account creation year
df['Account_creation_year'] = pd.to_datetime(df['Account_created_at']).dt.year
df

# Create a column with an account classification based on username filter
df['Suspicious_account'] = np.where(df['Username'].isin(usernames_filtered), True, False)
df
# Save dataframe as 'csv' file
df.to_csv('output/SeVan_processed.csv', index=False)

# Import Twitter Oauth keys from file
twitter_app_auth =  {
    'consumer_key': consumer_key,
    'consumer_secret': consumer_secret,
    'access_key': access_key,
    'access_secret': access_secret
    }

# Create an object for botometer
botometer = botometer.Botometer(mashape_key=rapidapi_key, wait_on_ratelimit=True, **twitter_app_auth)

# Evaluate accounts from list
results = []
for username, bot_score in botometer.check_accounts_in(usernames_filtered):
    results.append({username: bot_score})
len(results)
results

# Create a copy of results dictionary
dict_copy = results.copy()
dict_copy

# Get all evaluations on a list
evaluations = []
for i in range(len(dict_copy)):
    evaluations.append(dict_copy[i].get(usernames_filtered[i]))
evaluations

# Get cap evaluation on a list
cap = []
for i in range(len(evaluations)):
    cap.append(evaluations[i].get('cap'))
len(cap)
cap

# Get raw_scores evaluation on a list
raw_scores = []
for i in range(len(evaluations)):
    raw_scores.append(evaluations[i].get('raw_scores').get('english'))
len(raw_scores)
raw_scores

# Update cap list with raw_scores values
for i in range(len(cap)):
    cap[i].update(raw_scores[i])
cap

# Convert list to dataframe
df = pd.DataFrame(cap)
df

# Create a column from list
df.assign(username=usernames_filtered)
df

# Save dataframe as 'csv' file
df.to_csv('output/bots_sevan.csv', index=False)
