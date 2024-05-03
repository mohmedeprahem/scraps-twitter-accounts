from twikit.errors import TooManyRequests
from twikit import Client
import re
import time
from datetime import datetime, timedelta

def scrape_twitter(accounts, interval):
  client = Client('en-US')

  # Login and save/load cookies
  client.login(
    auth_info_1='MohamedIbr82388',
    password='@Mohmed123',
  )
  client.save_cookies('cookies.json')
  client.load_cookies(path='cookies.json')

  while True:
    mentions_count = {}
    interval_ago = datetime.now() - timedelta(seconds=interval)

    # Iterate over each account
    for account in accounts:
      try:
          user = client.get_user_by_screen_name(account)
          tweets = user.get_tweets('Tweets', count=100)

          cashtag_pattern = r'\$[A-Za-z]{3,4}'

          # Iterate over each tweet
          for tweet in tweets:
              interval_ago = datetime.now() - timedelta(seconds=interval)
              interval_ago = interval_ago.astimezone(tweet.created_at_datetime.tzinfo)  # Convert to the user's timezone

              # Check if the tweet is within the specified time interval
              if tweet.created_at_datetime > interval_ago:
                  matches = re.findall(cashtag_pattern, tweet.full_text)
                  for match in matches:
                      symbol = match.upper()
                      mentions_count[symbol] = mentions_count.get(symbol, 0) + 1
      except TooManyRequests:
        print("Rate limit exceeded. Waiting for 15 minutes before retrying...")
        time.sleep(15 * 60)
        continue

    for symbol, count in mentions_count.items():
      print(f"Number of mentions of {symbol}: {count}")
    print(f"Time interval used: {interval} seconds")
    print("===========================================")

    time.sleep(interval)

twitter_accounts = ['Mr_Derivatives', 'warrior_0719', 'ChartingProdigy', 'allstarcharts', 'yuriymatso', 'TriggerTrades', 'AdamMancini4', 'CordovaTrades', 'Barchart', 'RoyLMattox']
scraping_interval = 900



scrape_twitter(twitter_accounts, scraping_interval)

