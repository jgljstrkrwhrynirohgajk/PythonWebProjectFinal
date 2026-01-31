from app import app, render_template
import requests

@app.route('/admin/category')
def category():
    module = "category"
    return render_template('backend/category/index.html', module=module)
