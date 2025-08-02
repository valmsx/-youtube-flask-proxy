from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = "YOUR_API_KEY"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_WATCH_PLUGIN = "http://msx.benzac.de/plugins/youtube.html?id="

@app.route("/msx_search")
def msx_search():
    query = request.args.get("input", "").strip()
    if not query:
        return jsonify({
            "type": "pages",
            "headline": "YouTube Search",
            "template": {
                "type": "separate",
                "layout": "0,0,3,3",
                "color": "black",
                "imageFiller": "cover"
            },
            "items": []
        })

    # Effettua la ricerca YouTube
    params = {
        "q": query,
        "key": YOUTUBE_API_KEY,
        "part": "snippet",
        "maxResults": 10,
        "type": "video"
    }
    yt_response = requests.get(YOUTUBE_API_URL, params=params)
    data = yt_response.json()

    # Costruisci items compatibili MSX
    items = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        items.append({
            "title": snippet["title"],
            "playerLabel": snippet["title"],
            "image": snippet["thumbnails"]["high"]["url"],
            "action": f"video:plugin:{YOUTUBE_WATCH_PLUGIN}{video_id}"
        })

    return jsonify({
        "type": "pages",
        "headline": f"Risultati per '{query}'",
        "template": {
            "type": "separate",
            "layout": "0,0,3,3",
            "color": "black",
            "imageFiller": "cover"
        },
        "items": items
    })
