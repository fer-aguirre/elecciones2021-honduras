import pandas as pd
import numpy as np
import re
import datetime
import os
from oauth_keys import *
#!pip install botometer
import botometer


# Read 'csv' file as dataframe
df = pd.read_csv("output/NoVolveran.csv", index_col=None)
df

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
# Save dataframe as 'csv' file
df.to_csv('output/NoVolveran_processed.csv', index=False)

# Import Rapidapi key from environment variable
rapidapi_key = os.environ['RAPIDAPI_KEY']

# Import Twitter Oauth keys from file
twitter_app_auth =  {
    'consumer_key': TOKENS.get('consumer_key'),
    'consumer_secret': TOKENS.get('consumer_secret'),
    'access_key': TOKENS.get('access_key'),
    'access_secret': TOKENS.get('access_secret')}

# Create an object for botometer
botometer = botometer.Botometer(mashape_key=rapidapi_key, wait_on_ratelimit=True, **twitter_app_auth)

# Evaluate accounts from list
results = []
for username, bot_score in botometer.check_accounts_in(usernames):
    results.append({username: bot_score})
len(results)
results

dict_copy = results[i].copy()
# Get all evaluations on a list
evaluations = []
for i in range(len(results)):
    evaluations.append(results[i].get(usernames_filtered[i]))
evaluations

# Get cap evaluation on a list
cap = []
for i in range(len(evaluations)):
    cap.append(evaluations[i].get('cap'))
cap

# Convert list to dataframe
df = pd.DataFrame(cap)
# Save dataframe as 'csv' file
df.to_csv('output/bot_evaluation.csv', index=False)
