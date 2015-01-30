#coding=utf-8
import cherrypy
from cherrypy import tools
import json
import threading
import urllib
import time
import requests

## initialization and configuration
clientSleepTime = 1.0 # client thread sleep time
balls = {} # empty dictionary for saving the currently held balls
clientID = 'python-rest' # used for identifying our section of the payload
precedingServerURL = 'http://localhost:8080/balls'
ownServerURL = 'http://localhost:8080/balls'
checkInterval = 3 # the amount of seconds to wait before checking the preceding server for new balls
lastChecked = time.time() # the time we last checked the preceding server for new balls

def clientFunction():
	global lastChecked
	response = None
	# request balls every x seconds from the preceding server, specified via the checkInterval variable
	if time.time() > lastChecked + checkInterval:
		lastChecked = time.time()
		getBallsRequest = requests.get(precedingServerURL)
		if getBallsRequest.status_code == requests.codes.ok:
			response = getBallsRequest.json()  # implicit conversion from JSON to a dictionary
			if not response:  # check if dictionary is empty
				# print(str(lastChecked) + ': Received no new ball from preceding server.')  # for more verbose output
				pass # skip the output
			else:
				print(str(lastChecked) + ': Received new ball(s) from preceding server: ' + str(response))

				# generate timestamp of receiving time for hold time calculations
				timestamp = time.time()

				# iterate over newly received balls
				for id, ball in response.items():
					print('Processing ball ' + str(id) + '. Data: ' + str(ball))
					ball['hop-count'] = ball['hop-count'] + 1    # increase the hop count
					ball['payload'][clientID] = timestamp        # save the previously generated timestamp for hold time calculation
					balls[id] = ball
					requests.delete(precedingServerURL+'/'+id) # preceding server must delete sent balls

				print(str(lastChecked) + ': Newly received ball(s) processed.')
		else:
			print(str(lastChecked) + ': HTTP Error while getting new balls: code' + str(req.status_code) + ', reason: ' + req.reason)

    # compare the time-stamps and holdtime of entries in balls with the current time
    # if the current time is larger than the time-stamp and holdtime, the ball is send to the server with a PUT request
	for id, ball in list(balls.items()): 
		currentTime = time.time()
		lastHoldTime = ball['payload'][clientID]+ball['hold-time']
		if currentTime >= lastHoldTime:
			req = requests.request('PUT', ownServerURL+'/'+id, json = ball) # implicit conversion of ball into JSON
			print(str(currentTime) + ': Sending ball: ' + str(ball))
			if req.status_code == requests.codes.ok:		
				balls.pop(id, None)
			else:
				print(str(currentTime) + ': HTTP Error while sending ball: code ' + str(req.status_code) + ', reason : ' + req.reason)
				balls.pop(id, None) # normally, we should retry

	t = threading.Timer(clientSleepTime, clientFunction)
	t.start()

clientFunction()
