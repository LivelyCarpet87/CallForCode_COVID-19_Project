import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)


@app.route('/InitSelf/', methods=["POST"])
def recievePositiveReport():
    self = request.form['Self']
    secret = initNewUser(self)
    return jsonify(
        secret = secret
    )


@app.route('/positiveReport/', methods=["POST"])
def recievePositiveReport():
    positives = request.form['Positives']
    secret = request.form['Secret']
    valid = verifySecret(secret)
    if valid:
        markPositive(positives)

    return jsonify(
        msg = "Get well soon. "
    )


@app.route('/QueryMetMacAddr/', methods=["POST"])
def recieveQueryMetMacAddr():
    queries = request.form['Queries']
    queryAddr(queries)
    return jsonify(

    )


def initNewUser(self):
    pass


def verifySecret(secret):
    pass

def markPositive(positives):
    pass


def queryAddr(queries):
    pass


def parseMacAddr(AddrStr):
    pass

app.run()
