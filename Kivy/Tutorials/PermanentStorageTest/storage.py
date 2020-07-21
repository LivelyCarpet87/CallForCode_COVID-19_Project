from kivy.storage.jsonstore import JsonStore

#store = JsonStore('hello.json')

# put some values
#store.put('tito', name='Mathieu', org='kivy')
#store.put('tshirtman', name='Gabriel', age=27)

#print('Gabriel is', store.get('tshirtman')['age'])

# using the same index key erases all previously added key-value pairs
#store.put('tito', name='Mathieu', age=30)

# get a value using a index key and key
#print('tito is', store.get('tito')['age'])

# or guess the key/entry for a part of the key
#for item in store.find(name='Gabriel'):
#    print('tshirtmans index key is', item[0])
#    print('his key value pairs are', str(item[1]))


#store.put('testArray', arrValue=[3, 2, 7])
#print('Array is', store.get('testArray')["arrValue"])



#store = JsonStore('local.json')
#store.put("macDict", value = dict())
'''
class storageUnit():

    def __init__(self):
        self.store = JsonStore('local.json')
#        self.store.put("macDict", value = dict())
        
    def getStore(self):
        return self.store
    def addEntry(self, macAddress, time):
        if macAddress in self.store.get("macDict")["value"]:
            self.store.get("macDict")["value"][macAddress] += [time]#HEREEE
        else:
            self.store.get("macDict")["value"][macAddress] = [time]

x = storageUnit()


x.addEntry(1, 10)
x.addEntry(1, 20)
x.addEntry(2, 20)
x.addEntry(1, 30)
x.addEntry(3, 30)

y = storageUnit()

print(x.getStore().get("macDict")["value"][1])
print(x.getStore().get("macDict")["value"][2])
print(x.getStore().get("macDict")["value"][3])

print(y.getStore().get("macDict")["value"][1])
print(y.getStore().get("macDict")["value"][2])
print(y.getStore().get("macDict")["value"][3])



store = JsonStore('test.json')
print(store.exists("bob"))


import datetime

print(type(str(datetime.datetime.now())))
'''

store = JsonStore('0721.json')
store.put()
