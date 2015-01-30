# Installation
1. Make sure you have Python3 installed. 
2. The server requires the cherrypy framework and the client makes use of the requests library. You can install them via
```
pip install cherrypy requests
```
# Usage
## Server
Start the server via `python server.py`. It will wait for incoming requests and log them if needed. GET, PUT and DELETE requests can be made.

The list of currently held balls can be retrieved via GET request, e.g. `curl http://[server-ip]:8080/balls`. Said list will be returned as a JSON document with the MIME-Type application/json and be encoded in utf-8. It is structured as follows:
* when there is no ball in the list: `{}`
* when there is at least one ball in the list (here an example with 2 balls):
```json
{
	"1": {
		"hop-count": 4,
		"hold-time": 5,
		"payload": {
			"python-rest": 1422566976.839366,
			"client2" : 123456
			}
		},
	"testball" : {
		"hop-count": 2,
		"hold-time": 6,
		"payload": {
			"python-rest": 14225,
			"client2" : 65431
			}
	}
}
```
After retrieving balls from the server, they have to be deleted via DELETE request. The ball ID has to be specified in this case, e.g. `curl -X "DELETE" http://[server-ip]:8080/balls/testball`

New balls can be sent to the server via PUT request. The ball ID has to be specified in the URL and the ball content (hold-time, payload etc.) has to be stored in the request body.

##Client
Start the client via `python client.py`. Every x seconds, the client polls the preceding server for new balls. After their designated hold time, they are sent via PUT request to our server.
