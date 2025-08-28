import os
import time
import glob
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from tqdm import tqdm

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def authenticate_youtube():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=8080)
    return build("youtube", "v3", credentials=creds)

def get_existing_playlists(youtube):
    playlists = {}
    next_page_token = None

    while True:
        request = youtube.playlists().list(
            part="snippet",
            mine=True,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            title = item["snippet"]["title"]
            playlists[title.lower()] = item["id"]
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return playlists

def create_playlist(youtube, title, description="Imported by script"):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    return response["id"]

def search_video(youtube, query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=1
    )
    response = request.execute()
    items = response.get("items", [])
    if items:
        return items[0]["id"]["videoId"]
    return None

def get_existing_video_ids(youtube, playlist_id):
    video_ids = set()
    next_page_token = None

    while True:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response["items"]:
            vid = item["snippet"]["resourceId"]["videoId"]
            video_ids.add(vid)
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def add_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()

def main():
    youtube = authenticate_youtube()
    existing_playlists = get_existing_playlists(youtube)
    txt_files = glob.glob("*.txt")

    if not txt_files:
        print("❌ No .txt files found.")
        return

    for txt_file in txt_files:
        playlist_name = os.path.splitext(txt_file)[0].replace("_", " ").title()
        playlist_id = existing_playlists.get(playlist_name.lower())

        if playlist_id:
            print(f"📄 Found existing playlist: {playlist_name}")
        else:
            print(f"➕ Creating new playlist: {playlist_name}")
            playlist_id = create_playlist(youtube, playlist_name)
            existing_playlists[playlist_name.lower()] = playlist_id

        existing_videos = get_existing_video_ids(youtube, playlist_id)

        with open(txt_file, "r", encoding="utf-8") as f:
            songs = [line.strip() for line in f if line.strip()]

        not_found = []
        added_count = 0

        for song in tqdm(songs, desc=f"🎵 Updating '{playlist_name}'"):
            try:
                video_id = search_video(youtube, song)
                if not video_id:
                    not_found.append(song)
                    continue
                if video_id not in existing_videos:
                    add_to_playlist(youtube, playlist_id, video_id)
                    existing_videos.add(video_id)
                    added_count += 1
                    time.sleep(0.5)
            except Exception as e:
                print(f"⚠️ Error adding {song}: {e}")
                not_found.append(song)

        print(f"✅ {added_count} songs added to '{playlist_name}'")

        # Save failed ones
        if not_found:
            error_file = txt_file.replace(".txt", "_errors.txt")
            with open(error_file, "w", encoding="utf-8") as ef:
                ef.write("\n".join(not_found))
            print(f"⚠️ {len(not_found)} songs not found — saved in '{error_file}'")

if __name__ == "__main__":
    main()
