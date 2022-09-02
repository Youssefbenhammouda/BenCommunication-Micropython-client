
# BenCommunication-Micropython-client
A **client** library that runs on the micropython side to communicate with [BenCommunication Server](link.com).

The BenCommunication project uses UDP protocol to communicate with the server, it can assure a secure communication between Micropython and Python scripts over the network.
BenCommunication use AES CBC algorithm to encrypt the traffic with a key file that must be kept in a secure place.

**The library will:**

 - Generate a random iv for each request and send it along with the
   payload.
 - Generate a unique ID for each request.
## Installation
Download [benclient.py](link.com) and save it on the micropython main directory.

## Object arguments
benclient.client() can have the following arguments:
 1. host (str) => The ip of the server.
 2. port (int) => The port used by server.
 3. timeout (int) => (default=10) How much time to wait for response from server.
 4. keyfile (str) => (default=key.sec) the keyfile, it contains 32 random bytes. You can generate a key with the server module. .
 5. buffersize (int) => (default=4096) The buffer for Udp Socket.
 
 benclient.client().send() can have the following arguments:
 
 1. data (dict) : payload to be sent must be in following format `{ "action" : "someaction" ,"data" : ... }`
 2. noreturn (bool): (default=false) if set to True, it will wait for the return of the called action.

## Example to send data from sensor every 1 minute

    import dht from machine 
    import Pin
    from time import sleep
    from  benclient  import  client # Import the 
	obj  =  client("192.168.1.2",8585) # Server ip and port
    
    sensor = dht.DHT11(Pin(14)) #GPIO 14
    while True:
		sensor.measure() 
		temperature = sensor.temperature() 
		humidity = sensor.humidity()
		obj.send({"action":"dhtsensor","data":{
			"temperature":temperature , 
			"humidity":humidity 
			}}, noreturn=True) # We set noreturn to true, this will make library continue without waiting for response.
		sleep(60)
		
**If you have any suggestions, feel free to fork and send a pull request.**
**Thanks for reading :D**
  
 
