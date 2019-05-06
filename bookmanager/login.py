import os
import flask
from flask import render_template
import flask_login

app = flask.Flask(__name__)
app.secret_key = 'you have to change this sentence'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#mock database
users = {'foo@bar.tld':{'password': 'secret'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

# DO NOT ever store passwords in plaintext and always compare password
# hashes using constant-time comparison!
    user.is_authenticated = request.form['password']  == users[email]['password']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return render_template('login.html')

    email = flask.request.form['email'] 
    try:
        db_password = users[email]['password']
    except:
        message = 'email not found'    
        return render_template('login.html', message = message)

    if flask.request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return flask.redirect(flask.url_for('protected'))
    
    return 'Bad login'

@app.route('/protected') 
@flask_login.login_required
def protected():
    return 'Logged in as: '  + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'    

if __name__ == "__main__":
    app.run(debug=True)
    