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
        return "Retry"
    else:
        return "Unknown Issue Occurred"


def positiveReport(c,MacAddrSelf,secretKey):
    c.setopt(c.URL, baseURL+'PositiveReport')
    d = {}
    d['Positives'] = MacAddrSelf
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

    if code == 200 and "Get well soon. " in body:
        return "Server Ack Success"
    elif code != 200:
        return "Retry"
    else:
        return "Unknown Issue Occurred"


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

    if code == 200 and "Matched. " in body:
        return "Positive Match"
    elif code != 200:
        return "Retry"
    else:
        return "No Match"


def freeResources():
    c.close()
