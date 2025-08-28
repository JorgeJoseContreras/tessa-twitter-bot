#!/usr/bin/env python3
"""
Twitter Auto-Tweet Bot
Automatically posts a tweet once per day from a predefined list
"""

import tweepy
import random
import json
import os
from datetime import datetime

# Configuration - Set these as environment variables for security
API_KEY = os.getenv('TWITTER_API_KEY')
API_SECRET = os.getenv('TWITTER_API_SECRET')
ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN')

def load_tweets(filename='tweets.json'):
    """Load tweets from JSON file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('tweets', []), data.get('used_tweets', [])
    except FileNotFoundError:
        print(f"Error: {filename} not found. Creating sample file...")
        create_sample_tweets_file(filename)
        return [], []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return [], []

def save_used_tweets(used_tweets, filename='tweets.json'):
    """Save the list of used tweets back to file"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except:
        data = {'tweets': [], 'used_tweets': []}
    
    data['used_tweets'] = used_tweets
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def create_sample_tweets_file(filename='tweets.json'):
    """Create a sample tweets file"""
    sample_data = {
        "tweets": [
            "🌟 Starting the day with gratitude! What are you thankful for today?",
            "💡 Remember: Progress, not perfection. Every small step counts!",
            "🚀 Innovation happens when we dare to think differently.",
            "🌱 Growth mindset: Challenges are opportunities in disguise.",
            "☕ Good morning! May your coffee be strong and your Monday be short.",
            "🎯 Focus on what you can control, let go of what you can't.",
            "📚 Learning something new every day keeps the mind sharp!",
            "🌈 After every storm comes a rainbow. Keep pushing forward!"
        ],
        "used_tweets": []
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(sample_data, f, indent=2, ensure_ascii=False)
    
    print(f"Created sample {filename}. Please edit it with your own tweets!")

def authenticate_twitter():
    """Authenticate with Twitter API v2"""
    try:
        # Create API v2 client
        client = tweepy.Client(
            bearer_token=BEARER_TOKEN,
            consumer_key=API_KEY,
            consumer_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET,
            wait_on_rate_limit=True
        )
        
        # Test authentication
        me = client.get_me()
        print(f"Authenticated as: @{me.data.username}")
        return client
        
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def post_tweet(client, tweet_text):
    """Post a tweet"""
    try:
        response = client.create_tweet(text=tweet_text)
        print(f"Tweet posted successfully: {tweet_text}")
        print(f"Tweet ID: {response.data['id']}")
        return True
    except Exception as e:
        print(f"Error posting tweet: {e}")
        return False

def main():
    """Main function"""
    print(f"Twitter Bot running at {datetime.now()}")
    
    # Check for required environment variables
    required_vars = ['TWITTER_API_KEY', 'TWITTER_API_SECRET', 'TWITTER_ACCESS_TOKEN', 
                    'TWITTER_ACCESS_TOKEN_SECRET', 'TWITTER_BEARER_TOKEN']
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        print("Error: Missing environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these environment variables before running the script.")
        return
    
    # Load tweets
    tweets, used_tweets = load_tweets()
    
    if not tweets:
        print("No tweets found in tweets.json")
        return
    
    # Get available tweets (not yet used)
    available_tweets = [t for t in tweets if t not in used_tweets]
    
    # If all tweets are used, reset the used list
    if not available_tweets:
        print("All tweets have been used. Resetting...")
        used_tweets = []
        available_tweets = tweets
    
    # Select random tweet
    selected_tweet = random.choice(available_tweets)
    
    # Authenticate with Twitter
    client = authenticate_twitter()
    if not client:
        return
    
    # Post the tweet
    if post_tweet(client, selected_tweet):
        # Mark tweet as used
        used_tweets.append(selected_tweet)
        save_used_tweets(used_tweets)
        print("Tweet posted and marked as used.")
    else:
        print("Failed to post tweet.")

if __name__ == "__main__":
    main()