import streamlit as st
import matplotlib.pyplot as plt
from googleapiclient.discovery import build

plt.rcParams['font.family'] = 'DejaVu Sans'

# Function to fetch channel information
def get_channel_info(youtube, channel_id):
    request = youtube.channels().list(
        part='snippet',
        id=channel_id
    )
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['snippet']['title']
    else:
        return None

# Function to fetch video statistics for the latest five videos of a channel
def get_video_statistics(youtube, channel_id):
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='date',  # Get the latest videos first
        type='video',
        maxResults=5  # Get only the latest five videos
    )
    response = request.execute()

    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_title = item['snippet']['title']
        video_statistics = youtube.videos().list(
            part='statistics',
            id=video_id
        ).execute()
        videos.append({'title': video_title, 'views': int(video_statistics['items'][0]['statistics']['viewCount'])})

    return videos

# Function to compare two users based on total views and performance of their latest five videos
def compare_users(api_key, channel_id_1, channel_id_2):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Fetch channel names
    channel_name_1 = get_channel_info(youtube, channel_id_1)
    channel_name_2 = get_channel_info(youtube, channel_id_2)

    # Print channel names
    st.write("User 1 YouTube Channel:", channel_name_1)
    st.write("User 2 YouTube Channel:", channel_name_2)

    # Fetch channel statistics
    channel_1_stats = youtube.channels().list(
        part="statistics",
        id=channel_id_1
    ).execute()
    channel_2_stats = youtube.channels().list(
        part="statistics",
        id=channel_id_2
    ).execute()

    # Extract total views
    total_views_1 = int(channel_1_stats['items'][0]['statistics']['viewCount'])
    total_views_2 = int(channel_2_stats['items'][0]['statistics']['viewCount'])

    # Fetch video statistics for latest five videos
    videos_1 = get_video_statistics(youtube, channel_id_1)
    videos_2 = get_video_statistics(youtube, channel_id_2)

    # Extract video titles and views
    video_titles_1 = [video['title'] for video in videos_1]
    video_views_1 = [video['views'] for video in videos_1]
    video_titles_2 = [video['title'] for video in videos_2]
    video_views_2 = [video['views'] for video in videos_2]

    # Plot total views comparison
    st.write("Comparison of Total Views")
    fig1, ax1 = plt.subplots()
    ax1.bar([channel_name_1, channel_name_2], [total_views_1, total_views_2], color=['blue', 'green'])
    ax1.set_ylabel('Total Views')
    st.pyplot(fig1)

    # Plot performance of latest five videos
    st.write("Performance of Latest Five Videos")
    fig2, ax2 = plt.subplots()
    ax2.plot(video_titles_1, video_views_1, marker='o', linestyle='-', color='blue', label='User 1')
    ax2.plot(video_titles_2, video_views_2, marker='o', linestyle='-', color='green', label='User 2')
    ax2.set_xlabel('Video Title')
    ax2.set_ylabel('Views')
    ax2.set_title('Performance of Latest Five Videos')
    ax2.legend()
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig2)


def main():
    st.title("YouTube Channel Comparison")
    api_key = 'Your_API_Key'  # Add your API key here
    channel_id_1 = 'Channel_ID_1'  # Add your channel ID here
    channel_id_2 = 'Channel_ID_2'  # Add your channel ID here
    compare_users(api_key, channel_id_1, channel_id_2)

if __name__ == "__main__":
    main()
