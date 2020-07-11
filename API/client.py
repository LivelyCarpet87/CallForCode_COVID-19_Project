import pycurl
import sys
import json
import urllib.parse
import re
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

this = sys.modules[__name__]
this.__buffer_obj__ = BytesIO()
this.__baseURL__ = 'https://covidcontacttracerapp-smart-zebra-ua.mybluemix.net/'
#this.__baseURL__ = 'http://0.0.0.0:8000/'
this.__curlHandle__ = pycurl.Curl()

def initSelf(MacAddrSelf):
    c = this.__curlHandle__
    c.setopt(c.URL, this.__baseURL__+'InitSelf')
    d = {}
    d['Self'] = MacAddrSelf
    # Form data must be provided already urlencoded.
    postfields = json.dumps(d)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, this.__buffer_obj__.write)
    c.perform()

    code = c.getinfo(pycurl.HTTP_CODE)
    body = this.__buffer_obj__.getvalue().decode('utf-8')
    resetResources()
    if "Initiated." not in body and code == 201:
        try:
            secretPattern = re.compile(r'(\S{56})')
            jdata = json.loads(body)
            secret = jdata['Secret']
            secret = secretPattern.match(secret).group(1)  # sanitization
        except KeyError:
            return 1
    if code == 201:
        return secret
    elif code != 200:
        #  Retry
        return 2
    elif code == 400:
        return 3  # Permission denied due to initiated
    else:
        #  Unknown Error
        return 1


def positiveReport(MacAddrSelf,secretKey,metAddrList):
    c = this.__curlHandle__
    c.setopt(c.URL, this.__baseURL__+'positiveReport')
    d = {}
    d['Self'] = MacAddrSelf
    d['MetAddrList'] = metAddrList
    d['Secret'] = secretKey
    # Form data must be provided already urlencoded.
    postfields = json.dumps(d)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, this.__buffer_obj__.write)
    c.perform()

    code = c.getinfo(pycurl.HTTP_CODE)
    body = str(this.__buffer_obj__.getvalue())

    resetResources()

    if code == 201 and "Get well soon. " in body:
        #  Server Ack Success
        return 0
    elif code == 200:
        #  Retry
        return 2
    else:
        #  Unknown Issue Occurred
        return 1


def negativeReport(MacAddrSelf,secretKey):
    c = this.__curlHandle__
    c.setopt(c.URL, this.__baseURL__+'negativeReport')
    d = {}
    d['Self'] = MacAddrSelf
    d['Secret'] = secretKey
    # Form data must be provided already urlencoded.
    postfields = json.dumps(d)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, this.__buffer_obj__.write)
    c.perform()

    code = c.getinfo(pycurl.HTTP_CODE)
    body = str(this.__buffer_obj__.getvalue())

    resetResources()

    if code == 201 and "Stay healthy." in body:
        #  Server Ack Success
        return 0
    elif code == 200:
        #  Retry
        return 2
    else:
        #  Unknown Issue Occurred
        return 1


def queryMyMacAddr(self,secret):
    c = this.__curlHandle__
    c.setopt(c.URL, this.__baseURL__+'QueryMyMacAddr')
    d = {}
    d['Self'] = self
    d['Secret'] = secret
    # Form data must be provided already urlencoded.
    postfields = json.dumps(d)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, this.__buffer_obj__.write)
    c.perform()

    code = c.getinfo(pycurl.HTTP_CODE)
    body = str(this.__buffer_obj__.getvalue())

    resetResources()

    if code == 200 and '{"atRisk":true}' in body:
        #  Contacted Positive MAC Addr
        return 1
    elif code != 200:
        #  Retry
        return 2
    else:
        #  No Match
        return 0


def forgetUser(MacAddrSelf, secretKey):
    c = this.__curlHandle__
    c.setopt(c.URL, this.__baseURL__+'ForgetMe')
    d = {}
    d['Self'] = MacAddrSelf
    d['Secret'] = secretKey
    # Form data must be provided already urlencoded.
    postfields = json.dumps(d)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, this.__buffer_obj__.write)
    c.perform()

    code = c.getinfo(pycurl.HTTP_CODE)
    body = str(this.__buffer_obj__.getvalue())
    print(body)
    resetResources()

    if code == 201 and "Goodbye. " in body:
        #  Server Ack Success
        return 0
    elif code == 200:
        #  Retry
        return 2
    else:
        #  Unknown Issue Occurred
        return 1


def resetResources():
    c = this.__curlHandle__
    del this.__buffer_obj__
    this.__buffer_obj__ = BytesIO()
    c.reset()

def freeResources():
    c = this.__curlHandle__
    c.close()

def tests():
    self = "FF:11:2E:7A:5B:6A"
    others = "4F:11:2E:7A:5B:6A, 4F:1A:2E:7A:5B:6A, 4F:11:77:7A:5B:6A"
    person2 = "4F:11:2E:7A:5B:6A"
    secret1 = initSelf(self)
    secret2 = initSelf(person2)
    print(len(secret1)==56)
    print(queryMyMacAddr(self,secret1)==0)
    print(positiveReport(self,secret1,others)==0)
    print(queryMyMacAddr(person2,secret2)==0)
    print(negativeReport(self,secret1)==0)
    print(queryMyMacAddr(self,secret1)==0)
    print(forgetUser(self, secret1)==0)
    print(forgetUser(person2, secret2)==0)
    freeResources()

tests()
