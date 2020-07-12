import cloudant
from cloudant.client import Cloudant
from cloudant.document import Document
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
import json
import sys
"""
{
  "apikey": "***REMOVED***",
  "host": "***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-bluemix.***REMOVED***.appdomain.cloud",
  "iam_apikey_description": "Auto-generated for key ***REMOVED***-bdbe-41e1-b2ef-***REMOVED***",
  ***REMOVED***
  ***REMOVED***
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/***REMOVED***::serviceid:ServiceId-7e88976c-7e9e-4984-8e9b-b30d72df8b85",
  "url": "https://***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-bluemix.***REMOVED***.appdomain.cloud",
  "username": "***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-bluemix"
}
"""
# Useful variables
this = sys.modules[__name__]
this.__username__ = "***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-***REMOVED***-bluemix"
this.__apiKey__ = "***REMOVED***"
this.__client__ = None
this.__myDatabase__ = None
def init():
    # This is the name of the database we are working with.
    databaseName = "persons_db"

    client = Cloudant.iam(this.__username__, this.__apiKey__)
    client.connect()

    myDatabase = client.create_database(databaseName)
    if not myDatabase.exists():
        #  IDK, raise some error or panic
        client.create_database(databaseName)
    this.__client__ = client
    this.__myDatabase__ = myDatabase


def personExists(MAC_Addr):
    client = this.__client__
    myDatabase = this.__myDatabase__
    if not Document(myDatabase, MAC_Addr).exists():
        return False
    else:
        try:
            if getState(MAC_Addr) != None:
                return True
            else:
                return False
        except KeyError:
            return False


def addPerson(MAC_Addr,state,secretKey):
    #  Add a person if not already created
    client = this.__client__
    myDatabase = this.__myDatabase__
    if not personExists(MAC_Addr):
        data = {}
        data['_id'] = MAC_Addr
        data['State'] = state
        data['SecretKey'] = secretKey
        try:
            document = myDatabase.create_document(data, throw_on_exists=True)
            return True
        except cloudant.error.CloudantDatabaseException:
            changeState(MAC_Addr,state)
            changeSecretKey(MAC_Addr,secretKey)
            return True
    return False


def changeState(MAC_Addr,newState):
    # Edit or add user state
    client = this.__client__
    myDatabase = this.__myDatabase__
    if Document(myDatabase, MAC_Addr).exists():
        with Document(myDatabase, MAC_Addr) as document:
            document.field_set(document, 'State', newState)
            return True
    else:
        return False


def changeSecretKey(MAC_Addr,secretKey):
    # Edit or add user Secret Key
    client = this.__client__
    myDatabase = this.__myDatabase__
    if Document(myDatabase, MAC_Addr).exists():
        with Document(myDatabase, MAC_Addr) as document:
            document.field_set(document, 'SecretKey', secretKey)
            return True
    else:
        return False


def getState(MAC_Addr):
    client = this.__client__
    myDatabase = this.__myDatabase__
    if Document(myDatabase, MAC_Addr).exists():
        with Document(myDatabase, MAC_Addr) as document:
            document.fetch()
            return document['State']
    else:
        return None


def getSecretKey(MAC_Addr):
    client = this.__client__
    myDatabase = this.__myDatabase__
    if Document(myDatabase, MAC_Addr).exists():
        with Document(myDatabase, MAC_Addr) as document:
            document.fetch()
            return document['SecretKey']
    else:
        return None

def removePerson(MAC_Addr):
    client = this.__client__
    myDatabase = this.__myDatabase__
    if Document(myDatabase, MAC_Addr).exists():
        with Document(myDatabase, MAC_Addr) as document:
            document.delete()
            return True
    else:
        return False

def cloudantCleanup():
    client = this.__client__
    if client:
        client.disconnect()

def testCloudant():
    init()
    print("exists? \n")
    print(personExists("ab:bc:cd:de:ef:99"))
    print("add person \n")
    print(addPerson("ab:bc:cd:de:ef:99",4,""))
    print("exists? \n")
    print(personExists("ab:bc:cd:de:ef:99"))
    print(changeSecretKey("ab:bc:cd:de:ef:99", "supersecret"))
    print("get status \n")
    print(getState("ab:bc:cd:de:ef:99"))
    print(getSecretKey("ab:bc:cd:de:ef:99"))
    print(removePerson("ab:bc:cd:de:ef:99"))
    cloudantCleanup()

#testCloudant()