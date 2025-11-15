from app import app, render_template,request, redirect
import requests

app.secret_key = 'any_secret_key'  # Needed for flash messages
# 🔹 Replace with your actual Telegram Bot Token and Chat ID
BOT_TOKEN = '8574185655:AAFi_iiFZboj2KNDAnh1P_8g2FkcH-x6ApQ'
CHAT_ID = '@piseth99_bot'

@app.route('/contact')
def contact():  # put application's code here
    return render_template('contact.html')

@app.route('/send', methods=['POST'])
def send_message():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']

    text = f"""
📩 New Contact Form Message:
👤 Name: {name}
📧 Email: {email}
💬 Message: {message}
    """
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'

    payload = {
        'chat_id': CHAT_ID,
        'text': text
    }

    response = requests.post(url, json=payload)

    return redirect('/contact')