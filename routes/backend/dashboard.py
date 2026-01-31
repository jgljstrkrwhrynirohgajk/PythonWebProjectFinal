from app import app, render_template
import requests

@app.route('/admin')
def dashboard():
    module = 'dashboard'
    return render_template('backend/dashboard/index.html', module=module)