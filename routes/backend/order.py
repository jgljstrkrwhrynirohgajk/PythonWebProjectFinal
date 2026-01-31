from app import app, render_template
import requests

@app.route('/admin/order')
def order():
    module = 'order'
    return render_template('backend/order/index.html', module=module)