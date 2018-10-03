import cherrypy
import json

class toy(object):

    '''
    this class manages the state of the toy, that is simply a json
    '''

    def __init__(self):

        f = open('toy.txt')
        self.f_content = json.loads(f.read())
        self.state = self.f_content['state']
        f.close()

    def on(self):

        '''
        this method turns ON the toy
        '''

        f = open('toy.txt','w')
        self.f_content['state'] = 'ON'
        f.write(json.dumps(self.f_content))
        f.close()
        return 'The toy is ON'

    def off(self):

        '''
        this method turns OFF the toy
        '''

        f = open('toy.txt','w')
        self.f_content['state'] = 'OFF'
        f.write(json.dumps(self.f_content))
        f.close()
        return 'The toy is OFF'

    def check(self):

        '''
        this method checks the state of the toy
        '''

        f = open('toy.txt','r')
        self.f_content = json.loads(f.read())
        state = self.f_content['state']
        f.close()
        return 'The toy is %s' % state

class expose_toy(object):
    '''
    this class exposes the toy manager class
    '''

    exposed = True

    def __init__(self):

        self.my_toy=toy()

    def GET(self, *uri):

        if len(uri) != 1:
            return 'ERROR in inserting uri'
        else:
            if uri[0] == 'on':
                self.my_toy.on()
                return self.my_toy.on()
            elif uri[0] == 'off':
                return self.my_toy.off()
            elif uri[0] == 'check':
                return self.my_toy.check()
            else:
                return 'ERROR in command'

if __name__=='__main__':
    conf={
        '/':
        {'request.dispatch':cherrypy.dispatch.MethodDispatcher(),
        'tools.sessions.on':True
        }
    }
    cherrypy.tree.mount(expose_toy(),'/toy',conf)
    cherrypy.config.update({'server.socket_host':'0.0.0.0'})
    cherrypy.config.update({'server.socket_port':8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
