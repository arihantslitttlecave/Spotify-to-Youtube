

I recently made the full switch from **Spotify to YouTube Music**, and it wasn’t just random. I’d had enough of Spotify’s policies, shady internal decisions (yes, even the AI weaponry stuff 👀), and the way it’s been moving away from being for listeners.

Figuring out how to move my whole library wasn’t easy, but after some trial and error I finally managed to transfer everything, playlists, songs, the lot ( and thanks to the reddit posts that helped me out ).

Now, YouTube Music isn’t perfect (no platform is), but compared to Spotify it feels so much better: more flexible, bigger library, smoother integration. It’s not spotless, but it’s 100x better in my eyes. If you’re tired of Spotify’s nonsense, you might want to consider it too.
So here goes the whole process

< > **How does it work** :

The script acts like a bridge between your `.txt` playlist files and YouTube Music. Here’s the full flow explained simply but in detail:

1. **Authentication with Google (OAuth2)**
    
    - Google won’t let anyone change playlists without permission.
        
    - When you run the script, it opens a browser → you log in → Google gives your script a secure access token.
        
    - This token is saved in `token.json` so you don’t have to log in every time.
        
2. **Reading Your `.txt` Files**
    
    - Each `.txt` file represents one playlist.
        
    - The filename becomes the playlist name on YouTube.
        
    - Each line inside (e.g., `Joji - Glimpse of Us`) is treated as a song to add.
        
3. **Checking for Playlists on YouTube**
    
    - The script looks through your YouTube account to see if a playlist with that name already exists.
        
    - If it exists → it only adds new songs (skips duplicates).
        
    - If it doesn’t exist → it creates a new playlist automatically.
        
4. **Searching for Songs**
    
    - For each line in your `.txt`, the script calls the YouTube Data API’s **search endpoint**.
        
    - YouTube returns possible matches.
        
    - The script picks the first/best result and saves its video ID.
        
5. **Adding Songs to Playlists**
    
    - Once it has the video ID, the script tells YouTube: _“Insert this video into this playlist.”_
        
    - If the song is already in the playlist, it’s skipped.
        
    - If it can’t be added (not found, restricted, wrong match), it’s written to an error log file.
        
6. **Logging Results**
    
    - Each playlist has its own log file (e.g., `lofi_errors.txt`).
        
    - This way you know which songs couldn’t be matched.
        
    - The rest are safely added to your YouTube Music account.
        
7. **Re-running Anytime**
    
    - You can run the script again whenever you add or edit a `.txt` file.
        
    - Since it checks duplicates, you won’t get repeated songs.
        
    - It’s scalable → works with a handful or even 100+ playlists.
        

In short:  
`.txt file → script reads → Google login → YouTube search → create/update playlist → add songs → log errors`.


< > **Why this process works** :

Because it uses YouTube’s official **Data API** with proper authentication. Here’s the reasoning:

1. **Google OAuth2 Authentication**
    
    - Google gives the script permission to act _as you_ on your YouTube account.
        
    - This means the script isn’t “hacking” or bypassing anything — it’s officially authorized.
        
2. **YouTube Data API**
    
    - The API is the same tool apps like YouTube Studio or transfer services use.
        
    - It provides endpoints for:
        
        - Creating playlists
            
        - Searching videos (songs)
            
        - Adding/removing items in playlists
            
3. **Text Files as Input**
    
    - `.txt` files are simple, universal, and lightweight.
        
    - They give the script a clear list of what songs to look for.
        
4. **Smart Updating**
    
    - The script checks for existing playlists and duplicates before adding.
        
    - That’s why you can re-run it anytime without breaking your library.
        
5. **Error Logging**
    
    - Anything the API can’t find is logged instead of failing silently.
        
    - This makes it reliable and transparent.
        
6. **Automation vs Manual**
    
    - Doing this by hand would take days.
        
    - The script automates it by leveraging the API, so even 10,000+ songs get transferred consistently.
      

< > **What do i need before starting** :

Before you run the tool, make sure you have these:

1. **Python installed** → Version 3.10 or above (check with `python --version`).
    
2. **Required Python libraries** → `google-auth-oauthlib`, `google-api-python-client`, `tqdm`, `requests` (install via `pip install -r requirements.txt`).
    
3. **Google Cloud Credentials** → A `client_secret.json` file (OAuth2 credentials) downloaded from your Google Cloud Console.
    
4. **YouTube Music account** → Must be logged into the same Google account where you authorized the app.
    
5. **Playlist files** → `.txt` files containing song names (each line = one song).


< > **How do i set it up?** :

- **Get the project folder ready**
    
    - Put the script file (`yt_music_transfer.py`) and all your playlist `.txt` files in the same folder.
        
    - Each `.txt` file should have one song per line. Example:
        
        `Coldplay - Yellow Kendrick Lamar - HUMBLE Daft Punk - Get Lucky`
        
- **Install Python if you don’t have it**
    
    - Download from [python.org](https://www.python.org/downloads/) (make sure to check _“Add Python to PATH”_ during installation).
        
    - Verify installation by typing in terminal:
        
        `python --version`
        
- **Install the required libraries**
    
    - Open terminal in your project folder and run:
        
        `pip install -r requirements.txt`
        
    - If you don’t have a `requirements.txt`, install manually:
        
        `pip install google-auth google-auth-oauthlib google-api-python-client requests tqdm`
        
- **Set up Google credentials (super important)**
    
    - Go to [Google Cloud Console](https://console.cloud.google.com/).
        
    - Create a project → Enable **YouTube Data API v3**.
        
    - Go to **APIs & Services > Credentials** → Create **OAuth Client ID** → Choose “Desktop App.”
        
    - Download the JSON file and rename it to `client_secret.json`.
        
    - Place this `client_secret.json` file inside your project folder.
        
- **Run the script for the first time**
    
    - In terminal, navigate to your project folder:
        
        `cd path/to/your/folder py yt_music_transfer.py`
        
    - This will open a browser asking you to log in to your Google account.
        
    - Grant access → Once approved, the script saves a `token.json` (so you don’t need to log in every time).
        
- **Done – setup complete**
    
    - Now your tool is ready. Any `.txt` playlist you drop in the folder can be turned into a YouTube Music playlist just by running the script again.

< > **How do i set it up** :

- **Prepare your playlist files**
    
    - Make a `.txt` file for each playlist you want to transfer.
        
    - Example: `MyFavSongs.txt`
        
    - Each line = one song, written as `Artist - Song Title`.
        
        `Arctic Monkeys - Do I Wanna Know? Billie Eilish - Bad Guy Travis Scott - Sicko Mode`
        
- **Place them in the project folder**
    
    - Put all `.txt` files in the same folder where `yt_music_transfer.py` and `client_secret.json` are.
        
- **Run the script**
    
    - Open terminal inside that folder.
        
    - Run:
        
        `py yt_music_transfer.py`
        
- **Login (only first time)**
    
    - The first time, a browser window opens → log in to your Google account → allow permissions.
        
    - After that, the tool saves `token.json`, so you won’t need to log in again.
        
- **Script does its work**
    
    - For each `.txt` file, it:
        
        - Creates a new playlist in YouTube Music (same name as file).
            
        - Reads songs line by line.
            
        - Searches them on YouTube Music.
            
        - Adds the best match to the playlist.
            
        - Skips duplicates if already added.
            
        - Logs unfound songs into a separate `.log` file (so you know which ones failed).
            
- **Check your YouTube Music**
    
    - Open music.youtube.com → go to your library → you’ll see the newly created playlists with your songs.
        
- **Adding more songs later**
    
    - Just edit your `.txt` file or add a new one.
        
    - Run the script again.
        
    - It will update the playlist with any new songs without duplicating existing ones.


< > **What are some common error and fixes** :

- **Error:** `ModuleNotFoundError: No module named 'google_auth_oauthlib'`
    
    - **Cause:** The required Python packages are not installed.
        
    - **Fix:** Run `pip install -r requirements.txt` to install all dependencies.
        
- **Error:** Browser does not open for Google login
    
    - **Cause:** Default browser not set, or system blocking auto-launch.
        
    - **Fix:** Copy the authentication link shown in the terminal and paste it manually in your browser.
        
- **Error:** Playlist doesn’t appear in YouTube Music
    
    - **Cause:** You may have authenticated with the wrong Google account.
        
    - **Fix:** Delete `token.json` (which stores login data), then run the script again to log in with the correct account.
        
- **Error:** Some songs are missing after transfer
    
    - **Cause:** Songs might not exist on YouTube Music, or file formatting is unclear.
        
    - **Fix:** Check your `.txt` file → write songs as `Artist - Title` for best matches. Rare songs may simply not be available.

< > **Security note (Important)**:

This script requires **Google authentication** to create playlists on your behalf. That means two sensitive files are generated:

- **`client_secret.json`** → Your app’s Google credentials.
    
- **`token.json`** → Stores your personal login session.
    

These files are like **keys to your YouTube account**. If someone else gets them, they could access and modify your playlists.

To stay safe:

- Never share these files publicly (especially not on GitHub).
    
- If you accidentally uploaded them, delete the files and regenerate new credentials from Google Cloud Console.
    
- Keep them only on your own machine.
    

This ensures your account and music library remain private and secure.


That's all
Remember to drink water guys :)

