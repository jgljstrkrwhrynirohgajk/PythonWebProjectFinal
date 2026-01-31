from app import app, render_template
import requests

@app.route('/admin/user')
def user():
    module = 'user'
    return render_template('backend/user/index.html', module=module)
