import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

API_KEY = "AIzaSyCXP5L4iH389iGNm3e28ky0IkY08K7LWfs"  # Replace "YOUR_API_KEY_HERE" with your actual API key

def get_authenticated_service():
    return build("youtube", "v3", developerKey=API_KEY)

def get_trending_videos(service, channel_id, max_results=10, days=7):
    try:
        # Calculate start and end dates based on the desired duration
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days)

        response = service.search().list(
            part="snippet",
            type="video",
            channelId=channel_id,
            order="date",
            publishedAfter=start_date.isoformat() + "Z",
            publishedBefore=end_date.isoformat() + "Z",
            maxResults=max_results
        ).execute()

        return response['items']
    except HttpError as e:
        st.error("An HTTP error occurred. Please try again later.")
        st.stop()

def main():
    # Example: Retrieving trending videos for a specific channel
    channel_id = "UChVzP7gNOlkymoo000Y9_6Q"  # Replace "YOUR_CHANNEL_ID_HERE" with the actual channel ID

    # Authenticate the service with the provided API key
    youtube = get_authenticated_service()

    # Retrieve trending videos for the last 30 days
    trending_videos_30_days = get_trending_videos(youtube, channel_id, days=30)

    # Retrieve trending videos for the last 7 days
    trending_videos_7_days = get_trending_videos(youtube, channel_id, days=7)

    # Plotting
    if trending_videos_30_days and trending_videos_7_days:
        plt.figure(figsize=(20, 6))

        # Plot for the last 30 days
        plt.subplot(1, 2, 1)
        published_dates_30_days = [datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ") for video in trending_videos_30_days]
        plt.plot(published_dates_30_days, range(1, len(published_dates_30_days) + 1), marker='o')
        plt.gca().invert_yaxis()
        plt.xlabel('Published Date')
        plt.ylabel('Video Ranking')
        plt.title('Trending Videos Published Date (Last 30 Days)')

        # Plot for the last 7 days
        plt.subplot(1, 2, 2)
        published_dates_7_days = [datetime.strptime(video['snippet']['publishedAt'], "%Y-%m-%dT%H:%M:%SZ") for video in trending_videos_7_days]
        plt.plot(published_dates_7_days, range(1, len(published_dates_7_days) + 1), marker='o')
        plt.gca().invert_yaxis()
        plt.xlabel('Published Date')
        plt.ylabel('Video Ranking')
        plt.title('Trending Videos Published Date (Last 7 Days)')

        plt.tight_layout()

        st.pyplot(plt)

if __name__ == "__main__":
    main()
