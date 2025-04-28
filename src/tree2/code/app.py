from flask import Flask
from flask import render_template
from flask import request

from word_classifier import read_replacements
from word_classifier import replacements
import test
import time
import searcher

app = Flask(__name__, static_url_path='/static')

#"115582","Санкт-Петербург г, дор Кушелевская, 7 к. 6 литера А, кв. 431"


@app.route('/', methods=["GET", "POST"])
def index():
  #if request.method == 'GET':
  
  if request.method == 'POST':
    print(request.form.get('address'))

  return render_template('index.html')

@app.route('/hello/<name>')
def hello(name):
  return render_template('hello.html',name=name)


@app.route('/config/replacements')
def reconf_rep():
  read_replacements()
  return replacements

@app.route('/hello')
def hello_redir():
  return render_template('index.html')

@app.route('/search_by_class', methods=["POST"])
def search_by_class_req():
  print("Started search_by_class_req")
  print("Request:", request.get_json())
  
  resp_data = "placeholder"

  if request.method == 'POST':
    resp_data = request.get_json()
    addr_to_search = request.get_json()

    #csv_file = "./fias_dict/fias_dict.csv"

    results = searcher.get_address_by_classified(addr_to_search, test.tree_start)
    resp_data = results
    print(resp_data)

    return {"response" : resp_data}


@app.route('/search', methods=["POST"])
def search_req():
  resp_data = "placeholder"

  if request.method == 'POST':

    resp_data = request.get_json()['address']
    addr_to_search = request.get_json()['address']

    csv_file = "./fias_dict/fias_dict.csv"

    results = searcher.get_address(addr_to_search, test.tree_start)
    resp_data = results
    print(resp_data)

    return {"response" : resp_data}

@app.route('/about')
def about():
  return 'This is the about page \n <p><a href="/">Go back</a></p>'

if __name__ == '__main__':
  app.run(host="0.0.0.0", debug=True, port=5000)