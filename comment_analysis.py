from googleapiclient.discovery import build
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Function to fetch comments for a video
def get_comments_for_video(youtube, video_id):
    comments = []
    next_page_token = None

    while True:
        response = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            pageToken=next_page_token
        ).execute()

        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)

        next_page_token = response.get("nextPageToken")

        if not next_page_token:
            break

    return comments

# Function to analyze sentiment of comments
def analyze_sentiment(comments):
    from nltk.sentiment import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    sentiments = []

    for comment in comments:
        sentiment_score = sid.polarity_scores(comment)
        if sentiment_score['compound'] >= 0.05:
            sentiments.append('Positive')
        elif sentiment_score['compound'] <= -0.05:
            sentiments.append('Negative')
        else:
            sentiments.append('Neutral')

    return sentiments

# Function to suggest changes based on sentiment analysis
def suggest_changes(sentiments):
    positive_count = sentiments.count('Positive')
    negative_count = sentiments.count('Negative')
    total_comments = len(sentiments)

    positive_percentage = (positive_count / total_comments) * 100
    negative_percentage = (negative_count / total_comments) * 100

    return total_comments, positive_percentage, negative_percentage

# Function to plot sentiment distribution
def plot_sentiment_distribution(sentiments):
    sentiment_counts = {'Positive': 0, 'Negative': 0, 'Neutral': 0}

    for sentiment in sentiments:
        sentiment_counts[sentiment] += 1

    return sentiment_counts

# Main function to analyze YouTube channel
def analyze_youtube_channel(api_key, channel_id):
    st.title("YouTube Channel Analysis")

    youtube = build('youtube', 'v3', developerKey=api_key)
    channel_info = youtube.channels().list(
        part='snippet,statistics',
        id=channel_id
    ).execute()

    if 'items' in channel_info and channel_info['items']:
        channel_info = channel_info['items'][0]
        st.subheader("Channel Information")
        st.write("Channel Name:", channel_info['snippet']['title'])
        st.write("Subscriber Count:", channel_info['statistics']['subscriberCount'])

        video_data = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            maxResults=5
        ).execute()

        st.subheader("Videos Analysis")
        for item in video_data['items']:
            video_title = item['snippet']['title']
            video_id = item['id']['videoId']
            st.subheader("Video Title: " + video_title)

            comments = get_comments_for_video(youtube, video_id)
            sentiments = analyze_sentiment(comments)
            total_comments, positive_percentage, negative_percentage = suggest_changes(sentiments)

            st.write("Total Comments:", total_comments)
            st.write("Positive Comments:", f"{positive_percentage:.2f}%")
            st.write("Negative Comments:", f"{negative_percentage:.2f}%")
            
            st.subheader("Comments")
            st.write(comments)

            st.subheader("Sentiment Distribution")
            sentiment_counts = plot_sentiment_distribution(sentiments)
            labels = sentiment_counts.keys()
            values = sentiment_counts.values()

            fig, ax = plt.subplots()
            ax.bar(labels, values, color=['green', 'red', 'blue'])
            ax.set_xlabel('Sentiment')
            ax.set_ylabel('Count')
            ax.set_title('Sentiment Distribution')
            st.pyplot(fig)

# API Key and Channel ID
api_key = 'AIzaSyC-6kRzZ1_PSAuvBDQLe6GeD2r7IBG0ogI'
channel_id = 'UChVzP7gNOlkymoo000Y9_6Q'

analyze_youtube_channel(api_key, channel_id)
