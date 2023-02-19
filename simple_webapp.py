from flask import Flask, session
from checker import check_loggin

app = Flask(__name__)

app.secret_key = 'YouCanNeverGuessWhatMySecretKeyIs'

def do_check() -> bool:
  if 'logged_in' in session:
    return True
  return False

@app.route('/login')
def do_login() -> str:
  session['logged_in'] = True
  return 'You are now logged in.'

@app.route('/logout') 
def do_logout() -> str:
  session.pop('logged_in')
  return 'you are now logged out'

@app.route('/status')
def check_status() -> str:
  if 'logged_in' in session:
    return 'You are still logged in'
  return 'You Have been logged out'

@app.route('/')
def hello() -> str:
  return 'Hello from the simple web app'

@app.route('/page1')
@check_loggin
def page1() -> str:
  if not do_check():
    return 'You are not logged in'
  return 'this is page one'

@app.route('/page2')
@check_loggin
def page2() -> str:
  return 'this is page two'

@app.route('/page3')
@check_loggin
def page3() -> str:
  return 'this is page3'

if __name__ == '__main__':
  app.run(debug = True)