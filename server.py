#http://flask.pocoo.org/docs/0.11/quickstart/
# export FLASK_APP=server.py
# python -m flask run

from flask import Flask, render_template
from flask import request
from search import search



app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

@app.route('/ping')
def ping():
  return 'pong'

# http://127.0.0.1:5000/search?from_=Brno&to=Ostrava&date=2017-09-09
# http://127.0.0.1:5000/search?from_=Brno&to=Ostrava&date=2017-07-22
@app.route('/search', methods=['GET'])
def data():
  date = request.args.get('date')
  from_ = request.args.get('from_')
  to =  request.args.get('to')
  result = search(from_, to, date)
  return render_template('index.html', result=result)


@app.route('/')
def register():
    #http://127.0.0.1:5000/search?from_=Brno&to=Ostrava&from_=2017-09-09
    return render_template('search.html')





if __name__ == '__main__':
   app.run()
