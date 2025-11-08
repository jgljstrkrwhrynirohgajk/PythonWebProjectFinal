from app import app, render_template
import requests

@app.route('/shop')
@app.route('/shop')
def shop():
    try:
        response = requests.get('https://fakestoreapi.com/products', timeout=10)
        response.raise_for_status()  # Raises HTTPError if response code != 200
        data = response.json()       # May raise JSONDecodeError
    except requests.exceptions.RequestException as e:
        print("Request error:", e)
        data = []  # Empty fallback list
    except ValueError:
        print("Invalid JSON response from API")
        data = []

    return render_template('shop.html', products=data)
