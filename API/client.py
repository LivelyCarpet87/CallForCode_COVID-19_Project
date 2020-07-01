import pycurl
try:
    # python 3
    from urllib.parse import urlencode
except ImportError:
    # python 2
    from urllib import urlencode
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


b_obj = BytesIO()
baseURL='www.somesite.com/api/'
c = pycurl.Curl()


def initSelf(c,MacAddrSelf):
    c.setopt(c.URL, baseURL+'InitSelf')
    d = {}
    d['Self'] = MacAddrSelf
    post_data = json.dumps(d)
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()

    code = curl.getinfo(pycurl.HTTP_CODE)
    body = buffer.getvalue()

    c.reset()

    if code == 201:
        return body
    elif code != 200:
        #  Retry
        return 2
    else:
        #  Unknown Error
        return 1


def positiveReport(c,MacAddrSelf,secretKey):
    c.setopt(c.URL, baseURL+'positiveReport')
    d = {}
    d['Self'] = MacAddrSelf
    d['Secret'] = secretKey
    post_data = json.dumps(d)
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()

    code = curl.getinfo(pycurl.HTTP_CODE)
    body = buffer.getvalue()

    c.reset()

    if code == 201 and "Get well soon. " in body:
        #  Server Ack Success
        return 0
    elif code == 200:
        #  Retry
        return 2
    else:
        #  Unknown Issue Occurred
        return 1


ef negativeReport(c,MacAddrSelf,secretKey):
    c.setopt(c.URL, baseURL+'negativeReport')
    d = {}
    d['Self'] = MacAddrSelf
    d['Secret'] = secretKey
    post_data = json.dumps(d)
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()

    code = curl.getinfo(pycurl.HTTP_CODE)
    body = buffer.getvalue()

    c.reset()

    if code == 201 and "Stay healthy." in body:
        #  Server Ack Success
        return 0
    elif code == 200:
        #  Retry
        return 2
    else:
        #  Unknown Issue Occurred
        return 1


def queryMetMacAddr(c,MacAddrMet):
    c.setopt(c.URL, baseURL+'QueryMetMacAddr')
    d = {}
    d['Queries'] = MacAddrSelf
    post_data = json.dumps(d)
    # Form data must be provided already urlencoded.
    postfields = urlencode(post_data)
    # Sets request method to POST,
    # Content-Type header to application/x-www-form-urlencoded
    # and data to send in request body.
    c.setopt(c.POSTFIELDS, postfields)
    c.setopt(c.WRITEFUNCTION, buffer.write)
    c.perform()

    code = curl.getinfo(pycurl.HTTP_CODE)
    body = buffer.getvalue()

    c.reset()

    if code == 200 and '{"atRisk":true}' in body:
        #  Contacted Positive MAC Addr
        return 1
    elif code != 200:
        #  Retry
        return 2
    else:
        #  No Match
        return 0


def freeResources():
    c.close()
