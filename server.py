#coding=utf-8
import cherrypy
from cherrypy import tools
import time
balls = {}

def urldecode(url):
    #URLs are always latin-1, so we have to convert back to UTF-8
    return url.encode("latin-1").decode("utf-8")

class Balls(object):

    # make all methods available via URLs
    exposed = True
    
    @cherrypy.tools.json_out()  # all return values are automatically converted to JSON
    def GET(self, id=None):
        if id == None:
            if balls:
                print(str(time.time()) + ': Ball list requested. Sending: ' + str(balls)) # check if there are any balls before generating output
            return balls        # returns all currently held balls
        elif id in balls:
            ball = balls[id]
            if ball:
                print(str(time.time()) + ': Ball ' + str(id) + ' requested. Sending: ' + str(ball)) # check if there is a matching before generating output
            return ball         # returns a specific ball (not needed in game context)
        else:
            print(str(time.time()) + ': Ball ' + str(id) + ' requested. Not found.')
            return {}           # returns an empty response when a specifically requested ball doesn't exist

    @cherrypy.tools.json_in()   # all input values are automatically converted to JSON
    def PUT(self, id):
        balls[urldecode(id)] = cherrypy.request.json
        balls[urldecode(id)]['hop-count'] = balls[urldecode(id)]['hop-count'] + 1    # increase the hop count
        print(str(time.time()) + ': Ball ' + str(id) + ' received. Storing: ' + str(cherrypy.request.json))

    def DELETE(self, id):       # needed for deletion after a ball has been requested and therefore passed on to the next client
        balls.pop(urldecode(id), None)
        print(str(time.time()) + ': Ball ' + str(id) + ' deletion requested. Deleted.')

if __name__ == '__main__':

    cherrypy.tree.mount(
        Balls(), '/balls',  # connect the Balls class to the /balls URL
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()} # automatically dispatch request types (e.g. GET) to their corresponding method
        }
    )
    cherrypy.log.screen = None # for better logging control cherrypy standard logging is turned off
    cherrypy.engine.start()
    cherrypy.engine.block()