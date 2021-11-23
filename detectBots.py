import pandas as pd
import re
import datetime
import numpy as np

# Read 'csv' file as dataframe
df = pd.read_csv("output/NoVolveran.csv", index_col=None)
df

# Create a list with usernames posting the hashtag
usernames = list(df['Username'])

# Remove duplicates usernames
usernames = [i for n, i in enumerate(usernames) if i not in usernames[:n]]
sorted(usernames)

# Filter usernames with a serie of numbers at the end (at least 5)
usernames_filtered = list(map(lambda x: x[0], filter(None, map(lambda x: re.findall(r'(^.*\d{5})', x), usernames))))
usernames_filtered
len(usernames_filtered)

# Create a column with account creation year
df['Account_creation_year'] = pd.to_datetime(df['Account_created_at'])
df['Account_creation_year'] = df['Account_creation_year'].dt.year
df

# Create a column with an account classification based on username filter
df['Suspicious_account'] = np.where(df['Username'].isin(usernames_filtered), True, False)
# Save dataframe as 'csv' file
df.to_csv('output/NoVolveran_processed.csv', index=False)

# Filter data posted by a suspicious account
# suspicious_accounts = df.loc[df['Username'].isin(usernames_filtered)]
# suspicious_accounts
