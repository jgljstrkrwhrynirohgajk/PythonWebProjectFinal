from app import app, render_template
import requests

@app.route('/admin/customer')
def customer():
    module = 'customer'
    return render_template('backend/customer/index.html', module=module)
