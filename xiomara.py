from oauth_keys import *
import tweepy as tw
import pandas as pd
import numpy as np
import re

def main():

    # Oauth keys
    consumer_key = TOKENS.get('consumer_key')
    consumer_secret = TOKENS.get('consumer_secret')
    access_key = TOKENS.get('access_key')
    access_secret = TOKENS.get('access_secret')

    # Authentication with Twitter
    auth = tw.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    # API
    api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_errors=set([503]))

    # Define the search query
    query = '@XiomaraCastroZ -filter:retweets'

    tweets_list = []
    for tweet in tw.Cursor(api.search, q=query, tweet_mode='extended', result_type='mixed', count=100).items():
        tweets_list.append((tweet.full_text, tweet.created_at, tweet.id_str, tweet.retweet_count, tweet.favorite_count, tweet.entities["hashtags"], tweet.lang, tweet.in_reply_to_status_id_str, tweet.in_reply_to_user_id_str, tweet.in_reply_to_screen_name, tweet.is_quote_status, tweet.user.screen_name, tweet.user.description, tweet.user.followers_count, tweet.user.verified, tweet.user.location, f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}", f"https://twitter.com/user/status/{tweet.in_reply_to_status_id_str}"))


    # Show the amount of tweets found with this query
    print("Tweets loaded: ", len(tweets_list))

     # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(tweets_list,columns=['Text', 'Created_at', 'Tweet_id', 'RT_count', 'Fav_count', 'Hashtags', 'Language', 'Reply_to_status_id', 'Reply_to_user_id', 'Reply_to_user', 'Quoted_status', 'Username', 'Bio_description', 'User_followers_count', 'Account_verified', 'User_location', 'URL', 'URL_reply'])
    # Remove blank values for NaN
    tweets_df.replace(r'^\s*$', np.nan, regex=True)

    # Define username on query as filename
    filename = re.findall(r'^@(.*)\s', query)
    # Save the dataframe as a csv file
    tweets_df.to_csv(f'output/{filename[0]}.csv', index = False)
    #Show how the file was saved
    print("File saved as: ", f'{filename[0]}.csv')

if __name__ == "__main__":
    main()
