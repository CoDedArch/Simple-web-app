from flask import Flask, render_template, request,session
from vsearch import search_for_letters
from checker import check_loggin

from DBcm import UseDatabase

app = Flask(__name__) #this is the flask webapp object assigned to app
app.secret_key = 'MatterIsADoneDealForAnyOneThatMarriesMatter'
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'vsearch',
                          'password': 'kelvin',
                          'database': 'vsearchlogDb'}

def log_request(req: 'flask_request', res: str) -> None:
  """A function that takes in a flask request and a results and write it to a database"""
  
  with UseDatabase(app.config['dbconfig']) as cursor:
    _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL , (req.form['phrase'], 
                          req.form['letters'], 
                          req.remote_addr, 
                          str(req.user_agent.browser), 
                          res, ))

@app.route('/search4', methods=['POST']) #this is decorator of the route function
def do_search() -> str:
  """This decorated function returns the strings of letters that matches a given phrase"""
 
  phrase = request.form['phrase']
  letters= request.form['letters']
  title = 'Here are your results: '
  results = str(search_for_letters( phrase, letters ))
  try:
    log_request(request, results)
  except Exception as err:
    print('*****Logging Failed with this Error: ', str(err))
    
  return render_template('results.html',
                         the_title = title,
                         the_phrase = phrase,
                         the_letters = letters,
                         the_results = results,)


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
  return render_template('entry.html', 
                          the_title='Welcome to search4letters on the Web!')

@app.route('/viewlog')
@check_loggin
def view_the_log() -> 'html':
  with UseDatabase(app.config['dbconfig']) as cursor:
    _SQL = """select phrase, letters, ip, browser_string, results
              from log
           """ 
    cursor.execute(_SQL)
    contents = cursor.fetchall()
  titles = ('Phrase','Letters', 'Remote_addr', 'User_agent', 'Results')
  return render_template('viewlog.html', 
                          the_title = 'View Log',
                          the_row_titles=titles,
                          the_data = contents,)

@app.route('/login')
def do_login() -> str:
  session['logged_in'] = True
  return 'You are now logged in'

@app.route('/logout')
def do_logout() -> str:
  session.pop('logged_in')
  return 'You are now logged out'

if __name__ == '__main__':
  app.run(debug = True)