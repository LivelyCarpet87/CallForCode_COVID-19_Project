import flask
from flask import request, jsonify
from flask_api import status
import sqlite3
import re
import json
import hashlib
import os

isMacAddr = re.compile(r"([\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2})")
isFloodAddr = re.compile("FF:FF:FF:FF:FF:FF",re.I)

connPos = sqlite3.connect('Positives.db')
cursPos = connPos.cursor()
connSec = sqlite3.connect('Secrets.db')
cursSec = connSec.cursor()

cursPos.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='positive' ''')
#if the count is 1, then table exists
if cursPos.fetchone()[0] != 1 : {
	cursPos.execute("create table positive (MAC_Addr)")
}
connPos.commit()
cursSec.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='secrets' ''')
#if the count is 1, then table exists
if cursSec.fetchone()[0] != 1 : {
	cursSec.execute("create table secrets (MAC_Addr, Secret_Key)")
}
connSec.commit()


app = flask.Flask(__name__)


#  Takes in a POST request with a json object containing a SINGLE MAC address
#  Returns a secret key based on the MAC address and a HTTP Code 201
#  Stores a copy of secret in the local database
@app.route('/InitSelf', methods=["POST"])
def initSelf():
    data = request.get_json(force=True)
    self = data['Self']
    selfList = parseMacAddr(self)
    if not selfList:
        return 'Bad MAC Address!', 400
    secret = initNewUser(selfList)
    if secret is not None:
        return jsonify(
            Secret = secret
        ), status.HTTP_201_CREATED
    else:
        return 'Already Initiated. ', 400


#  Takes in a POST request with a json object containing a SINGLE MAC address and a secret key
#  Returns a HTTP 201 and a msg = "Get well soon." message in JSON
@app.route('/positiveReport', methods=["POST"])
def receivePositiveReport():
    data = request.get_json(force=True)
    self = data['Self']
    secret = data['Secret']
    metAddrList = data['MetAddrList']
    addrList = parseMacAddr(self+", "+metAddrList)
    if not addrList:
        return 'Bad MAC Address!', 400
    valid = verifySecret(addrList[0],secret)
    if valid:
        markPositive(addrList)
        return jsonify(
            msg = "Get well soon. "
        ), status.HTTP_201_CREATED
    else:
        return 'Received', status.HTTP_200_OK


#  Takes in a POST request string with MAC addresses in CSV format
#  Returns a Boolean atRisk status in JSON
@app.route('/QueryMyMacAddr', methods=["POST"])
def receiveQueryMyMacAddr():
    data = request.get_json(force=True)
    self = data['Self']
    secret = data['Secret']
    if not verifySecret(self,secret):
        return 'Bad Request Key', 403
    addrList = parseMacAddr(self)
    if not addrList:
        return 'Bad MAC Address!', 400
    state = queryAddr(addrList[0])
    return jsonify(
        atRisk = state
    ), status.HTTP_200_OK


#  Takes in a POST request with a json object containing a SINGLE MAC address and a secret key
#  Returns a HTTP 201 and a msg = "Stay healthy." message in JSON
@app.route('/negativeReport', methods=["POST"])
def receiveNegativeReport():
    data = request.get_json(force=True)
    self = data['Self']
    secret = data['Secret']
    addr = parseMacAddr(self)
    if not addr:
        return 'Bad MAC Address!', 400
    valid = verifySecret(addr[0],secret)
    if valid:
        markNegative(addr[0])
        return jsonify(
            msg = "Stay healthy. "
        ), status.HTTP_201_CREATED
    else:
        return 'Received', status.HTTP_200_OK


@app.route('/ForgetMe', methods=["POST"])
def forgetSelf():
    data = request.get_json(force=True)
    self = data['Self']
    secret = data['Secret']
    addr = parseMacAddr(self)
    if not addr:
        return 'Bad MAC Address!', 400
    valid = verifySecret(addr[0],secret)
    if valid:
        deleteUser(addr[0],secret)
        return jsonify(
            msg = "Goodbye. "
        ), status.HTTP_201_CREATED
    else:
        return 'Received', status.HTTP_200_OK


def initNewUser(selfList):
    connPos = sqlite3.connect('Positives.db')
    cursPos = connPos.cursor()
    connSec = sqlite3.connect('Secrets.db')
    cursSec = connSec.cursor()

    addr = selfList[0]
    secret = None

    cursSec.execute("select * from secrets where MAC_Addr=:MAC_Addr", {"MAC_Addr": addr,} )
    match = cursSec.fetchone()

    if not match:
        secret = hashlib.sha224((addr+str(os.urandom(128))).encode('utf-8')).hexdigest()
        cursSec.execute("insert into secrets values (?, ?)", (addr, secret))
        connSec.commit()

    connPos.close()
    connSec.close()
    return secret


def verifySecret(addr, secret):
    connPos = sqlite3.connect('Positives.db')
    cursPos = connPos.cursor()
    connSec = sqlite3.connect('Secrets.db')
    cursSec = connSec.cursor()

    safetyCheck = re.compile(r'^([a-z0-9]{56})$')
    try:
        safeSecret = safetyCheck.fullmatch(str(secret)).group(1)
    except AttributeError:
        return False
    if not safeSecret:
        return False

    cursSec.execute("select * from secrets where MAC_Addr=:MAC_Addr and Secret_Key=:Secret_Key", {"MAC_Addr": addr, "Secret_Key": secret})
    match = cursSec.fetchone()

    connPos.close()
    connSec.close()
    if match is None:
        return False
    else:
        return True


def markPositive(addrList):
    connPos = sqlite3.connect('Positives.db')
    cursPos = connPos.cursor()
    connSec = sqlite3.connect('Secrets.db')
    cursSec = connSec.cursor()
    for positive in addrList:
        cursPos.execute("select * from positive where MAC_Addr=:MAC_Addr", {"MAC_Addr": positive,})
        match = cursPos.fetchone()
        if not match:
            cursPos.execute("insert into positive values (?)", (positive, ))
            connPos.commit()
    connPos.close()
    connSec.close()


def markNegative(negative):
    connPos = sqlite3.connect('Positives.db')
    cursPos = connPos.cursor()
    connSec = sqlite3.connect('Secrets.db')
    cursSec = connSec.cursor()

    cursPos.execute("delete from positive where MAC_Addr=:MAC_Addr",  {"MAC_Addr": negative,})
    connPos.commit()

    connPos.close()
    connSec.close()


def deleteUser(user, secret):
    connPos = sqlite3.connect('Positives.db')
    cursPos = connPos.cursor()
    connSec = sqlite3.connect('Secrets.db')
    cursSec = connSec.cursor()

    cursPos.execute("delete from positive where MAC_Addr=:MAC_Addr",  {"MAC_Addr": user,})
    connPos.commit()
    cursSec.execute("delete from secrets where MAC_Addr=:MAC_Addr and Secret_Key=:Secret_Key",  {"MAC_Addr": user,"Secret_Key": secret})
    connSec.commit()

    connPos.close()
    connSec.close()


def queryAddr(addr):
    connPos = sqlite3.connect('Positives.db')
    cursPos = connPos.cursor()
    connSec = sqlite3.connect('Secrets.db')
    cursSec = connSec.cursor()


    cursPos.execute("select * from positive where MAC_Addr=:addr", {"addr": addr})
    match = cursPos.fetchone()
    connPos.close()
    connSec.close()
    if match is not None:
        return True
    else:
        return False


def parseMacAddr(AddrStr):
    #sanitization of all input
    addrList = re.findall(isMacAddr,AddrStr)
    for addr in addrList:
        if re.match(isFloodAddr,addr) is not None:
            addrList.remove(addr)
    return addrList

#app.run()
