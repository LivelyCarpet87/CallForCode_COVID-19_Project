import flask
from flask import request, jsonify
import sqlite3
import json

app = flask.Flask(__name__)


@app.route('/InitSelf', methods=["POST"])
def initSelf():
    data = request.get_json(force=True)
    self = data['Self']
    secret = initNewUser(self)
    return jsonify(
        secret = secret
    )


@app.route('/positiveReport', methods=["POST"])
def recievePositiveReport():
    data = request.get_json(force=True)
    positives = data['Positives']
    secret = data['Secret']
    valid = verifySecret(secret)
    if valid:
        markPositive(positives)

    return jsonify(
        msg = "Get well soon. "
    )


@app.route('/QueryMetMacAddr', methods=["POST"])
def recieveQueryMetMacAddr():
    data = request.get_json(force=True)
    queries = data['Queries']
    queryAddr(queries)
    return jsonify(

    )


def initNewUser(self):
    return "superKey"


def verifySecret(secret):
    pass

def markPositive(positives):
    pass


def queryAddr(queries):
    pass


def parseMacAddr(AddrStr):
    pass

app.run()
