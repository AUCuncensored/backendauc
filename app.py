from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import re
import tweepy  # Import the tweepy library
from PIL import Image, ImageDraw, ImageFont
import uuid  # For generating unique filenames

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to the log file
LOG_FILE_PATH = 'messages.log'  # You can change the file name as needed
IMAGE_STORAGE_PATH = 'generated_images'  # Directory to save images

# Ensure the image storage directory exists
if not os.path.exists(IMAGE_STORAGE_PATH):
    os.makedirs(IMAGE_STORAGE_PATH)

# Twitter API credentials
TWITTER_API_KEY = 'S64ujlogShQJwuuAgwaxVymwR'
TWITTER_API_SECRET_KEY = 'xlyVTgkkhoQ3vBXKoQh1bEhDHFvRcjRuq2LQ4HksbtNLUajYgq'
TWITTER_ACCESS_TOKEN = '1842581688678809600-Ih26VgEWGSOHvpMpKAWok5L6zSMf49'
TWITTER_ACCESS_TOKEN_SECRET = 'lrS2zUqYVHnHY2SlZShdkdKRFY3CprcXNd1fu9U1SNwwj'
TWITTER_BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAI39wAEAAAAAEJs342DO5rCLEviecESlRf%2FBN88%3DlW3g7dJ1LnuNtpfkUjSyypVbpCERlMZuyukehSQp4FXtBM0os0"

# Set up Twitter API client
client = tweepy.Client(
    TWITTER_BEARER_TOKEN, 
    TWITTER_API_KEY, 
    TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)


@app.route('/api/messages', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message')
    year = data.get('year')  # Get the year from the request data
    major = data.get('major')  # Get the major from the request data

    # Get the user's IP address and user-agent
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    if message:
        try:
            tweet_content = f"Message: {message}\n{major} / {year}"
            response = client.create_tweet(text=tweet_content)
            print("Successfully posted to Twitter.")
        except Exception as e:
            print(f"Failed to post to Twitter: {e}")

        return jsonify({"status": "success", "message": "Message received, image generated, and posted to Twitter!"}), 200
    else:
        return jsonify({"status": "error", "message": "No message provided!"}), 400

if __name__ == '__main__':
    # Ensure the log file exists
    if not os.path.exists(LOG_FILE_PATH):
        open(LOG_FILE_PATH, 'w').close()
    app.run()
