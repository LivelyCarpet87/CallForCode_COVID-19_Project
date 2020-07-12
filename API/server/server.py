import flask
from flask import request, jsonify
from flask_api import status
import re
import json
import hashlib
import os
import time
import atexit

import CustomCloudantModules as ccm

isMacAddr = re.compile(r"([\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2}:[\da-f|A-F]{2})")
isFloodAddr = re.compile("FF:FF:FF:FF:FF:FF",re.I)


ccm.init()

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
	if secret == "":
		return 'Already Initiated. ', 403
	elif secret is None:
		return status.HTTP_500_INTERNAL_SERVER_ERROR
	else:
		return jsonify(
			Secret = secret
		), status.HTTP_201_CREATED



#  Takes in a POST request with a json object containing a SINGLE MAC address and a secret key
#  Returns a HTTP 201 and a msg = "Get well soon." message in JSON
@app.route('/positiveReport', methods=["POST"])
def receivePositiveReport():
	data = request.get_json(force=True)
	self = data['Self']
	secret = data['Secret']
	metAddrList = data['MetAddrList']
	self = parseMacAddr(self)
	metAddrList = parseMacAddr(metAddrList)
	if not metAddrList or not self:
		return 'Bad MAC Address!', 400
	valid = verifySecret(self[0],secret)
	if valid:
		markPositive(metAddrList, self[0])
		return jsonify(
			msg = "Get well soon. "
		), status.HTTP_201_CREATED
	else:
		return 'Incorect Secret Key', 403


#  Takes in a POST request string with MAC addresses in CSV format
#  Returns a Boolean atRisk status in JSON
@app.route('/QueryMyMacAddr', methods=["POST"])
def receiveQueryMyMacAddr():
	data = request.get_json(force=True)
	self = data['Self']
	secret = data['Secret']
	addrList = parseMacAddr(self)
	if not addrList:
		return 'Bad MAC Address!', 400
	if not verifySecret(addrList[0],secret):
		return 'Bad Request Key', 403
	state = queryAddr(addrList[0],secret)
	if state == 1:
		return jsonify(
			 atRisk = True
			 ), status.HTTP_200_OK
	elif state == 0:
		return jsonify(
				 atRisk = False
				 ), status.HTTP_200_OK
	elif state == -1:
		return 'No such user or invalid keys', 403
	else:
		return status.HTTP_500_INTERNAL_SERVER_ERROR



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
		markNegative(addr[0], secret)
		return jsonify(
			msg = "Stay healthy. "
		), status.HTTP_201_CREATED
	else:
		return 'Incorect Secret Key', 403


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
		return 'Incorect Secret Key', 403


def initNewUser(selfList):
	addr = selfList[0]
	secret = ""
	if not ccm.personExists(addr):
		secret = hashlib.sha224((addr+str(os.urandom(128))).encode('utf-8')).hexdigest()
		success = ccm.addPerson(addr,4,secret)  # States: 1. Recovered, 2. Positive, 3. Contacted, 4. Neutral
		if not success:
			raise cloudant.error.CloudantDatabaseException
	else: #person, exists, but may not be initiated. This only occurs if person contacted a person marked positive
		if ccm.getState(addr) == 3 and ccm.getSecretKey(addr) == "":
			secret = hashlib.sha224((addr+str(os.urandom(128))).encode('utf-8')).hexdigest()
			success = ccm.changeSecretKey(addr,secret)
			if not success:
				raise cloudant.error.CloudantDatabaseException
	return secret


def verifySecret(addr, secret):
	safetyCheck = re.compile(r'^([a-z0-9]{56})$')
	try:
		safeSecret = safetyCheck.fullmatch(str(secret)).group(1)
	except AttributeError:
		return False
	if not ccm.personExists(addr):
		return False
	if not safeSecret:
		return False
	if secret == ccm.getSecretKey(addr):
		return True
	else:
		return False


def markPositive(addrList, self):
	for positive in addrList:
		if ccm.personExists(positive):  # Change state if person exists
			# retry the write to the database up to 10 times if it fails
			attempt = 1
			while attempt <= 10:
				success = ccm.changeState(positive,3)
				time.sleep(1)  # Delay to prevent reaching free tier IBM Cloudant limits
				if success:
					break
				else:
					attempt = attempt + 1
		else:
			# if person not exist, create an unintiated Person with state
			attempt = 1
			while attempt <= 10:
				success = ccm.addPerson(positive,3,"")
				time.sleep(1)  # Delay to prevent reaching free tier IBM Cloudant limits
				if success:
					break
				else:
					attempt = attempt + 1


def markNegative(negative,secret):
	if not verifySecret(negative,secret):  # Do nothing if secret key does not match
		return None
	ccm.changeState(negative,1)  # Mark person as recovered


def deleteUser(user, secret):
	if not verifySecret(user,secret):  # Do nothing if secret key does not match
		return None
	ccm.removePerson(user)


def queryAddr(addr, secret):
	if not verifySecret(addr,secret):  # Do nothing if secret key does not match
		return -1  # return 403 forbidden incorrect secret or user not exist
	if ccm.getState(addr) == 3:
		return 1
	return 0


def parseMacAddr(AddrStr):
	#sanitization of all input
	addrList = re.findall(isMacAddr,AddrStr)
	for addr in addrList:
		if re.match(isFloodAddr,addr) is not None:
			addrList.remove(addr)
	return addrList


@atexit.register
def shutdown():
	ccm.cloudantCleanup()


port = int(os.getenv('PORT', 8000))
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=False)
