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

def log_message(message, ip_address, user_agent, year, major):
    """Append the message, IP, and user-agent to a log file."""
    with open(LOG_FILE_PATH, 'a') as log_file:
        log_file.write(f'Message: {message}\n')
        log_file.write(f'IP Address: {ip_address}\n')
        log_file.write(f'User-Agent: {user_agent}\n')
        log_file.write(f'Year: {year}\n')  # Log the year
        log_file.write(f'Major: {major}\n')  # Log the major
        log_file.write('-----------------------------------\n')


def create_image(message, year, major):
    """Create an image with the given message, year, and major."""
    
    # Set image size and colors
    width, height = 1080, 1080  # Instagram post size (1080x1080 pixels)
    background_color = (240, 240, 240)  # Light grey background
    border_color = (0, 123, 255)  # Blue border color
    text_color = (0, 0, 0)  # Black text
    box_color = (255, 255, 255)  # White box for message background

    # Create a blank image
    image = Image.new('RGB', (width, height), background_color)
    
    # Load a background image or fill with a color (optional)
    # Uncomment and update the path if you have a background image to use
    # try:
    #     background = Image.open('path/to/your/background.jpg').resize((width, height))
    #     image.paste(background)
    # except Exception as e:
    #     print(f"Could not load background image: {e}")
    
    draw = ImageDraw.Draw(image)

    # Load a font (you may need to adjust the path to a valid font file)
    try:
        font_title = ImageFont.truetype("arial.ttf", 70)  # Title font size
        font_body = ImageFont.truetype("arial.ttf", 50)  # Body text font size
    except IOError:
        font_title = ImageFont.load_default()  # Fallback to default font
        font_body = ImageFont.load_default()

    # Combine major and year for the title
    title_text = f"{major} / {year}"
    title_width, title_height = draw.textsize(title_text, font=font_title)
    title_position = ((width - title_width) / 2, 50)  # Increased top margin
    draw.text(title_position, title_text, fill=text_color, font=font_title)

    # Calculate the box size for the message
    message_box_padding = 30  # Padding for larger box
    message_box_width = 0.9 * width  # 90% of the image width
    message_box_x0 = (width - message_box_width) / 2
    message_box_y0 = 150 + title_height + 30  # Start below the title text with increased padding
    message_box_x1 = message_box_x0 + message_box_width
    message_box_y1 = message_box_y0 + 600  # Increased height for the message box

    # Draw a rounded rectangle for the message
    rounded_box_radius = 50  # Radius for rounded corners
    draw.rounded_rectangle([message_box_x0, message_box_y0, message_box_x1, message_box_y1], 
                            fill=box_color, outline=border_color, width=3, radius=rounded_box_radius)

    # Adjust font size for the message to fill the box
    font_size = 55  # Start with a larger font size for the message
    while True:
        try:
            font_body = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font_body = ImageFont.load_default()
        message_width, message_height = draw.textsize(message, font=font_body)

        if message_width < (message_box_width - 2 * message_box_padding) and message_height < (message_box_y1 - message_box_y0 - 2 * message_box_padding):
            break  # Stop if it fits
        font_size -= 1  # Decrease font size to fit the box

    # Calculate the position to center the message text in the box
    message_x = (message_box_x0 + message_box_width / 2) - (message_width / 2)
    message_y = (message_box_y0 + message_box_y1) / 2 - (message_height / 2)

    # Draw the message text centered in the box
    draw.text((message_x, message_y), message, fill=text_color, font=font_body)

    # Generate a unique filename using UUID
    unique_id = uuid.uuid4()  # Generate a random UUID
    image_path = os.path.join(IMAGE_STORAGE_PATH, f'generated_image_{unique_id}.png')

    # Save the image
    image.save(image_path)

    return image_path  # Return the path of the saved image

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

        # Generate an image
        image_path = create_image(message, year, major)
        print(f"Image saved as {image_path}")

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
    app.run(debug=True)
