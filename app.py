from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.route("/")
def home():
    return "YouTube Proxy API is running."

@app.route("/search")
def search():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": 10
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        return jsonify({"error": "YouTube API error"}), 500

    data = res.json()
    results = [
        {
            "title": item["snippet"]["title"],
            "videoId": item["id"]["videoId"],
            "thumbnail": item["snippet"]["thumbnails"]["medium"]["url"]
        }
        for item in data.get("items", [])
    ]
    return jsonify(results)

@app.route("/msx")
def msx():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query"}), 400

    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": 10
    }

    res = requests.get(url, params=params)
    if res.status_code != 200:
        return jsonify({"error": "YouTube API error"}), 500

    data = res.json()
    items = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        thumbnail = f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        action = f"video:plugin:http://msx.benzac.de/plugins/youtube.html?id={video_id}"

        items.append({
            "title": title,
            "playerLabel": title,
            "image": thumbnail,
            "action": action
        })

    msx_response = {
        "type": "pages",
        "headline": "YouTube",
        "template": {
            "type": "separate",
            "layout": "0,0,3,3",
            "color": "black",
            "imageFiller": "cover"
        },
        "items": items
    }

    response = make_response(jsonify(msx_response))
    response.headers["Content-Type"] = "application/json"
    return response
