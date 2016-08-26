from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import json
import os
from Twitter_friends import getDirectConnection

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def first():
    return render_template('base.html')

@app.route('/get_username',methods=['POST'])
def get_username():
    authKeys = json.load(open('static/OAUTHs.json', 'r'))
    director = getDirectConnection(request.form['user'], authKeys)
    nodes,links = director.makeNetwork()
    return jsonify(nodes=nodes,links=links)

if __name__ == '__main__':
    print 'running from the root'
    os.chdir(os.getcwd())
    app.secret_key = 'super-secret-key'
    app.debug = True
    app.run(host='0.0.0.0',port=5000)