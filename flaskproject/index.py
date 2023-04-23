from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bf02ad1b9eea7cca6a456b508ab369b7'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# In a real application, you would likely use a database to store and authenticate users
# For the sake of simplicity, we will hard-code a single user
class User(UserMixin):
    def __init__(self, id):
        self.id = id

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'lb' and password == 'lb@123':
            user = User(1)
            login_user(user)
            response = make_response(redirect(url_for('secret')))
            response.set_cookie('auth_token', 'bf02ad1b9eea7cca6a456b508ab369b7')
            return response
        else:
            message = 'Invalid credentials. Please try again.'
            return render_template('login.html', message=message)
    else:
        return render_template('login.html')

@app.route('/secret')
@login_required
def secret():
    return render_template('secret.html')

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    response = make_response(redirect(url_for('login')))
    response.set_cookie('auth_token', '', expires=0)
    return response

if __name__ == '__main__':
    app.run(debug=True)
