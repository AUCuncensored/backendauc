from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tweepy
from PIL import Image, ImageDraw, ImageFont
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the path to the log file
LOG_FILE_PATH = 'messages.log'
IMAGE_STORAGE_PATH = 'generated_images'

# Ensure the image storage directory exists
if not os.path.exists(IMAGE_STORAGE_PATH):
    os.makedirs(IMAGE_STORAGE_PATH)

# Twitter API credentials (keep them secure)
TWITTER_API_KEY = 'your-twitter-api-key'
TWITTER_API_SECRET_KEY = 'your-twitter-api-secret'
TWITTER_ACCESS_TOKEN = 'your-twitter-access-token'
TWITTER_ACCESS_TOKEN_SECRET = 'your-twitter-access-token-secret'
TWITTER_BEARER_TOKEN = "your-twitter-bearer-token"

# Set up Twitter API client
client = tweepy.Client(
    TWITTER_BEARER_TOKEN, 
    TWITTER_API_KEY, 
    TWITTER_API_SECRET_KEY,
    TWITTER_ACCESS_TOKEN,
    TWITTER_ACCESS_TOKEN_SECRET
)

@app.route('/', methods=['GET'])
def home():
    return "Flask API is running", 200

@app.route('/api/messages', methods=['POST'])
def receive_message():
    data = request.json
    message = data.get('message')
    year = data.get('year')
    major = data.get('major')

    if message:
        try:
            tweet_content = f"Message: {message}\n{major} / {year}"
            response = client.create_tweet(text=tweet_content)
            print("Successfully posted to Twitter.")
        except Exception as e:
            print(f"Failed to post to Twitter: {e}")

        return jsonify({"status": "success", "message": "Message received and posted to Twitter!"}), 200
    else:
        return jsonify({"status": "error", "message": "No message provided!"}), 400

if __name__ == '__main__':
    if not os.path.exists(LOG_FILE_PATH):
        open(LOG_FILE_PATH, 'w').close()
    app.run()
