from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

def search_youtube(query, max_results=10):
    params = {
        "part": "snippet",
        "q": query,
        "key": YOUTUBE_API_KEY,
        "maxResults": max_results,
        "type": "video"
    }
    response = requests.get(YOUTUBE_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()
    items = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        snippet = item["snippet"]
        title = snippet["title"]
        player_label = title
        thumbnail = snippet["thumbnails"]["high"]["url"]
        action = f"video:plugin:http://msx.benzac.de/plugins/youtube.html?id={video_id}"
        items.append({
            "title": title,
            "playerLabel": player_label,
            "image": thumbnail,
            "action": action
        })
    return items

@app.route('/msx_search')
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
    try:
        items = search_youtube(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    result = {
        "type": "pages",
        "headline": f"Risultati per '{query}'",
        "template": {
            "type": "separate",
            "layout": "0,0,3,3",
            "color": "black",
            "imageFiller": "cover"
        },
        "items": items
    }
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
