from twikit.errors import TooManyRequests
from twikit import Client
import re
import time
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def login_client():
  client = Client('en-US')
  try:
    if os.path.exists('cookies.json'):
      client.load_cookies(path='cookies.json')
      print("Cookies loaded successfully.")
    else:
      print("No existing cookie file found. Performing login...")
      perform_login(client)
      client.load_cookies(path='cookies.json')
  except:
    print("Failed to login. Try again later...")

  return client


def perform_login(client):
  client.login(
    auth_info_1=os.getenv('TWITTER_USERNAME'),
    password=os.getenv('TWITTER_PASSWORD'),
  )
  client.save_cookies('cookies.json')
  print("Login successful. Cookies saved.")

  return client
def scrape_twitter(accounts, interval):
  client = login_client()

  while True:
    mentions_count = {}

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
scraping_interval = 3600

scrape_twitter(twitter_accounts, scraping_interval)

