import yt_dlp
import os
import time
import requests
from mutagen.flac import FLAC, Picture
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def embed_thumbnail(audio_file, thumbnail_file):
    audio = FLAC(audio_file)
    picture = Picture()
    with open(thumbnail_file, 'rb') as img:
        picture.data = img.read()
    picture.type = 3  # Front cover
    picture.mime = 'image/png'  # or 'image/jpeg'
    picture.desc = 'Cover'
    audio.add_picture(picture)
    audio.save()
    return audio_file

def download_audio(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'ffmpeg_location': 'C:\\ffmpeg\\ffmpeg-7.0.2-essentials_build\\bin',  # Ensure this points to your ffmpeg location
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'flac',
                'preferredquality': '1411',
            },
            {
                'key': 'EmbedThumbnail',
            },
            {
                'key': 'FFmpegMetadata',
            },
        ],
        'writethumbnail': True,  # This option will download the thumbnail
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        title = info_dict.get('title', None)
        audio_file = f"downloads/{title}.flac"
        thumbnail_file = f"downloads/{title}.jpg"  # yt-dlp downloads as jpg

        if os.path.exists(audio_file):
            return audio_file, title

        ydl.download([url])

        if os.path.exists(audio_file) and os.path.exists(thumbnail_file):
            embed_thumbnail(audio_file, thumbnail_file)

        return audio_file, title

@app.route("/api/download", methods=['GET'])
def get_download():
    video_id = request.args.get('id', '')
    audio_file, title = download_audio(video_id)
    if audio_file:
        return jsonify({"url": f"https://abcd1234.ngrok.io/api/downloads/{os.path.basename(audio_file)}"})
    else:
        return jsonify({"error": "Failed to download audio"}), 500

@app.route('/api/downloads/<filename>', methods=['GET'])
def download_file(filename):
    path = f"downloads/{filename}"
    if os.path.exists(path):
        print(f"File exists: {filename}")  # Debug print
        return send_from_directory('downloads', os.path.basename(path), as_attachment=True)
    else:
        print(f"File not found: {filename}")  # Debug print
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    # Start Flask server
    from threading import Thread
    def run_flask():
        app.run(host='0.0.0.0', port=8080)
    Thread(target=run_flask).start()
    # Wait a bit for the server to start
    time.sleep(5)
    # Make an initial dummy request to the ngrok URL to bypass the intro screen
    requests.get('https://abcd1234.ngrok.io')
