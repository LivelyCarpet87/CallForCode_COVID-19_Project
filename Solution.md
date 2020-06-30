# List of Resources for getting Mac Addresses

## Online Tools / Apps

1.  Wifi 分析仪

	1. [Github Repo](https://github.com/alexxy/netdiscover)

	2. Using "arp -a" to get recorded ip and mac address

	    1. (Question) Pinging the ip address will save to arp?

2. App Interface

3. API

	1. Mobile
	
		1. Uses python curl library
	
	2. Server
	
		1. Uses python 

	3. Protocol
		1. Query
		
			1. Query with GET request with a csv file of MAC addresses
		
			2. Server replies with a risk assesment string and 200 OK
		
		2. Diagnosis
			1. Post a request with a csv of associated MAC addresses, with a secret key
			2. Server responds with 200 OK
			
		3. Malformed request
		
			1. Server responds with error code for invalid csv data
			
			2. incorrect key responds with error message
			
			3. lack of key respond with 200 OK but ignore
			
		4. malformed response retry until limit reached, then delay. 

4. Database


