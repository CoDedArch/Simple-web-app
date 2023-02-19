#i want to create a decorator
from flask import session
from functools import wraps

#name of decorator be check_loggin
def check_loggin(func: object) -> object:
  #have to decorate this function to 
  @wraps(func)
  def wrapper(*args, **kwargs):
    if 'logged_in' in session:
      return func(*args, **kwargs)
    return 'You are not logged in!!'
  return wrapper