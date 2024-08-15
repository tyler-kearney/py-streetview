import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
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

def run():
    @app.route('/', methods=["GET", "POST"])
    def index():
        if request.method == "POST":
            address = request.json("address")
            image_fn = streetview_data(address)
            return render_template("index.html", images=image_fn)
        return render_template("index.html")
    app.run(debug=True)

class MainWindow:
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PyStreetView")
        self.setGeometry(600, 480)
        
        # Create a webview
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("http://127.0.0.1:5000"))
        
        # Create a layout
        layout = QVBoxLayout()
        layout.addWidget(self.webview)
        
        central_widget = QWidget = QWidget()
        central_widget.setLayout(layout)
        self.CentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    window=MainWindow()
    window.show()
    sys.exit(app.exec())