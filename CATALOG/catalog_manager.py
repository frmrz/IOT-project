from threading import Thread
import cherrypy
import json
import time
import datetime
import requests

class catalog_manager():

    '''
    this class manages the catalog in order to update and retrieve information about it
    '''

    def __init__(self, file):

        '''
        this method initializes the attributes "broker" and "actors", acquiring
        them from the catalog file determined when creating the instance of the class
        '''

        catalog_file=open(file,'r')
        catalog_content=json.load(catalog_file)
        self.broker=catalog_content['broker'] #dict with information about the broker
        self.actors=catalog_content['actors'] #dict with information about actors
        self.users=catalog_content['users'] #list of dicts containing usernames and passwords
        catalog_file.close()

    def print_catalog(self):

        '''
        this method prints the whole catalog content
        '''
        #initializing the list of ACTIVE actors
        active_list = []

        active_actors_list = self.actors['active']
        for active_actor in active_actors_list:
            active_list.append(active_actor['type'] + ' ' + active_actor['ID'])

        #initializing the list of REGISTERED actors
        registered_list = []

        registered_actors_list = self.actors['registered']
        for registered_actor in registered_actors_list:
            registered_list.append(registered_actor['type'] + ' ' + registered_actor['ID'])

        #initializing the list of USERS
        usersID = []

        for i in range(len(self.users)):
            usersID.append(self.users[i]['userID'])

        msg=(
        '''
        Network settings:
        Broker: %s
        Port: %d

        -------------------
        ACTIVE DEVICES:

        %s

        -------------------
        REGISTERED DEVICES:

        %s

        -------------------
        USERS:

        %s

        '''
        ) % (self.broker['host'],self.broker['port'],json.dumps(active_list),json.dumps(registered_list),json.dumps(usersID))

        return msg

class catalog_config():

    exposed = True

    def GET(self, *uri, **params):

        '''
        the GET method is used to retrieve information about the catalog
        '''

        if uri[0] == 'print_catalog':
            return catalog_manager('catalog.json').print_catalog()

    def POST(self, *uri, **params):

        '''
        the POST method is used to update catalog information
        '''

        now=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #read the body content
        body_payload=cherrypy.request.body.read()
        new_data_dict=json.loads(body_payload)
        new_data_dict["last_update"]=now

        #save in a variable the content of the catalog
        catalog = open('catalog.json','r').read()
        catalog_dict = json.loads(catalog)

        if uri[0]=='imalive':

            '''
            checks the actors in the catalog, registers the new actuator if it's
            not present, only updates its timestamp if it's present
            '''

            registered_actors_list = catalog_dict['actors']['registered']
            active_actors_list = catalog_dict['actors']['active']

            #Check if the actor is already registered
            if not any((actor['type']+actor['ID'])==(new_data_dict['type']+new_data_dict['ID']) for actor in registered_actors_list):

                #if it's not registered, information in the catalog is now updated with current timestamp
                registered_actors_list.append(new_data_dict)
                active_actors_list.append(new_data_dict)

                catalog_dict['actors']['registered']=registered_actors_list
                catalog_dict['actors']['active'] = active_actors_list

                new_catalog=open('catalog.json','w')
                new_catalog.write(json.dumps(catalog_dict, indent=4))
                new_catalog.close()

                msg=(
                '''
                New device added to register and updated
                ------------------------
                New catalog:
                %s
                '''
                ) % json.dumps(catalog_dict, indent=4)

                return msg

            else: #if the actor is already registered

                #updating the timestamp in the registered actors list
                for i in range(len(registered_actors_list)):
                    if registered_actors_list[i]["type"]+registered_actors_list[i]["ID"]==new_data_dict["type"]+new_data_dict["ID"]:
                        registered_actors_list[i]["last_update"]=now

                #checking if it's active
                if any((actor['type']+actor["ID"])==(new_data_dict["type"]+new_data_dict["ID"]) for actor in active_actors_list):

                    #if it's active, update the timestamps
                    for i in range(len(active_actors_list)):
                        if active_actors_list[i]["type"]+active_actors_list[i]["ID"]==new_data_dict["type"]+new_data_dict["ID"]:
                            active_actors_list[i]["last_update"]=now

                else: #if it's not active

                    #add it to the active actors list
                    active_actors_list.append(new_data_dict)

                #updating the catalog file
                catalog_dict['actors']['active'] = active_actors_list

                new_catalog=open('catalog.json','w')
                new_catalog.write(json.dumps(catalog_dict, indent=4))
                new_catalog.close()

                msg=(
                '''
                Device updated
                --------------------------
                Current catalog:
                %s
                '''
                ) % json.dumps(catalog_dict, indent=4)

                return msg

class actor_removal(Thread):

    '''
    this thread class will remove from the active actors list in the catalog actors
    not active for more than a given time
    '''

    def __init__(self, catalog_name, time_to_live):

        Thread.__init__(self)
        self.daemon = True
        self.time_to_live = time_to_live
        self.catalog_name = catalog_name
        self.start()

    def run(self):

        while True:

            #get the information from the catalog
            old_catalog = open(self.catalog_name, 'r').read()
            old_catalog_dict = json.loads(old_catalog)
            actor_list = old_catalog_dict['actors']['active']

            now_time = time.time() #save the current POSIX timestamp
            remove_list = [] #initialize the list of actors to remove

            for actor in actor_list:

                #compare the current timestamp with the last update of every actor
                last_update=actor["last_update"]

                #convert the string timestamp in POSIX format
                fmt = '%Y-%m-%d %H:%M:%S'
                d1 = datetime.datetime.strptime(last_update, fmt)
                old_time = time.mktime(d1.timetuple())

                #calculate the inactivity time of the actuator
                time_diff=now_time-old_time

                #remove it if it's bigger than a given time (contained in conf.json)
                if time_diff > self.time_to_live:
                    remove_list.append(actor['type']+actor['ID'])

            #initialization of the updated actor list
            new_list = []
            #initialization of the list of removed actors
            removed_actors = []

            #creation of the new list
            for actor in actor_list:

                if (actor['type']+actor['ID']) in remove_list:
                    #actor is put in the list of removed actors
                    removed_actors.append(actor)

                else:
                    #actor is put in the updated list
                    new_list.append(actor)

            #save the new catalog with the updated list
            old_catalog_dict['actors']['active'] = new_list

            new_catalog=open('catalog.json','w')
            new_catalog.write(json.dumps(old_catalog_dict, indent=4))
            new_catalog.close()

            #the process repeats after a given time (the same as before)
            time.sleep(self.time_to_live)

if __name__ == '__main__':

    #when the program starts, reads the information in the conf.json file, containing
    #the name of the catalog, the time_to_live and the address of host and port
    file_conf=open('conf.json','r')
    catalog_conf=json.load(file_conf)
    catalog_name=catalog_conf['catalog']
    time_to_live=catalog_conf['time_to_live']
    host = catalog_conf['host']
    port = catalog_conf['port']
    file_conf.close()

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
        }
    }

    #start the thread to remove actors older than a given time in the catalog
    actor_removal(catalog_name, time_to_live)

    cherrypy.server.socket_host = host
    cherrypy.server.socket_port = port
    cherrypy.tree.mount (catalog_config(), '/', conf)
    cherrypy.engine.start()
    cherrypy.engine.block()
