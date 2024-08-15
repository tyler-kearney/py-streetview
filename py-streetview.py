import sys
import webview
from flask import Flask, render_template, request, jsonify
import geocoder
import google_streetview

app = Flask(__name__)

def streetview_data(address):
    # Geocode the address
    geo = geocoder.google(address)
    if geo.ok:
        lat, lng = geo.latlng
        
        # Fetch streetview image
        api_key = "AIzaSyAkdYYXm2EBigNb7xAlSoS_zGt-tsJsJDM"
        params = [
            {
                "size": "600x480",
                "location": f"{lat}, {lng}",
                "heading": "0",
                "pitch": "0",
                "key": api_key
            }
        ]
        results = google_streetview.api.results(params)
        return results.download_links()
    else:
        return None

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        address = request.json("address")
        image_fn = streetview_data(address)
        return render_template("index.html", images=image_fn)
    return render_template("index.html")

def start_app():
    app.run(debug=True)

if __name__ == "__main__":
    webview.create_window("PyStreetView", "http://127.0.0.1:5000")
    webview.start(start_app)