from app import app, render_template
import requests

@app.route('/')
@app.route('/home')
def home():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0 Safari/537.36"
    }
    try:
        response = requests.get('https://fakestoreapi.com/products', headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        data = []

    return render_template('index.html', products=data)