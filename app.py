from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tweepy

app = Flask(__name__)
CORS(app)  # Allow all origins for simplicity; restrict this in production.

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

LOG_FILE_PATH = 'messages.log'  # Define your log file path

def log_message(message, ip_address, user_agent, year, major):
    """Append the message, IP, and user-agent to a log file."""
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(f'Message: {message}\n')
        log_file.write(f'IP Address: {ip_address}\n')
        log_file.write(f'User-Agent: {user_agent}\n')
        log_file.write(f'Year: {year}\n')  # Log the year
        log_file.write(f'Major: {major}\n')  # Log the major
        log_file.write('-----------------------------------\n')

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
        log_message(message, ip_address, user_agent, year, major)  # Log the message, year, and major
        print(f"Received message: {message}, Year: {year}, Major: {major}")

        # Generate an image if necessary (optional step)
        # image_path = create_image(message, year, major)
        # print(f"Image saved as {image_path}")

        # Post to Twitter (only text)
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
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)