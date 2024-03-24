import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from googleapiclient.discovery import build
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression

# Function to fetch channel statistics
def get_channel_statistics(youtube, channel_id):
    request = youtube.channels().list(
        part="statistics",
        id=channel_id
    )
    response = request.execute()
    if 'items' in response:
        return response['items'][0]['statistics']
    else:
        return None

# Function to fetch the number of subscribers gained in the last month
def get_subscriber_gain_last_month(youtube, channel_id):
    current_time = datetime.now()
    start_of_current_month = datetime(current_time.year, current_time.month, 1)
    start_of_previous_month = start_of_current_month - timedelta(days=1)
    start_of_previous_month = datetime(start_of_previous_month.year, start_of_previous_month.month, 1)

    # Fetch subscriber count for the start of current and previous month
    current_month_stats = get_channel_statistics(youtube, channel_id)
    previous_month_stats = get_channel_statistics(youtube, channel_id)

    # Calculate subscriber gain
    current_subscribers = int(current_month_stats['subscriberCount'])
    previous_subscribers = int(previous_month_stats['subscriberCount'])
    subscriber_gain = current_subscribers - previous_subscribers

    return subscriber_gain

# Function to predict future subscriber gain
def predict_future_subscriber_gain(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch current subscriber count
    channel_stats = get_channel_statistics(youtube, channel_id)
    current_subscribers = int(channel_stats['subscriberCount'])

    # Fetch subscriber gain in the last month
    subscriber_gain_last_month = get_subscriber_gain_last_month(youtube, channel_id)

    # Assuming a linear growth trend, let's fit a simple linear regression model
    X = np.array([[0], [1]])  # Representing months
    y = np.array([current_subscribers, current_subscribers + subscriber_gain_last_month])  # Subscribers count
    model = LinearRegression().fit(X, y)

    # Predict future subscriber count for next month
    future_month = 2  # Assuming next month
    future_subscriber_count = model.predict([[future_month]])[0]

    return future_subscriber_count

# Function to visualize predicted subscribers count for next month
def visualize_prediction(api_key, channel_id):
    youtube = build('youtube', 'v3', developerKey=api_key)

    current_subscribers = int(get_channel_statistics(youtube, channel_id)['subscriberCount'])
    predicted_subscribers = predict_future_subscriber_gain(api_key, channel_id)

    # Line chart
    plt.figure(figsize=(8, 6))
    plt.plot([0, 1], [current_subscribers, predicted_subscribers], marker='o', linestyle='-', color='blue')
    plt.xticks([0, 1], ['Current Subscribers', 'Predicted Subscribers Next Month'])
    plt.ylabel('Subscribers Count')
    plt.title('Current and Predicted Subscribers')
    plt.grid(True)

    # Streamlit display
    st.pyplot(plt)

# Example usage
api_key = 'YOUR_API_KEY'
channel_id = 'YOUR_CHANNEL_ID'

# Streamlit UI
st.title('YouTube Subscribers Prediction')
st.write('Predicting subscribers for the next month based on current data.')

# Displaying the prediction graph
visualize_prediction(api_key, channel_id)
