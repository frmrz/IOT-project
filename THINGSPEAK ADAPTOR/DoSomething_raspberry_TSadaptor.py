from MyMQTT import MyMQTT
import json
import cherrypy
import time
import requests

class Thingspeak_REST():
    def __init__(self):
        pass;

    def GETINVOCATION(self,dato,field):
        url = "https://api.thingspeak.com/update?api_key=0KZDXE6HNBVENWTQ&field";
        req = requests.get(url+ '%d=' %field +str(dato));
		print (url+ '%d=' %field +str(dato));

class DoSomething():

	def __init__(self, clientID):
		# create an instance of MyMQTT class
		self.messaggio = '';
		self.clientID = clientID
		self.myMqttClient = MyMQTT(self.clientID, "iot.eclipse.org", 1883, self)

	def run(self):
		# if needed, perform some other actions befor starting the mqtt communication
		print ("running %s" % (self.clientID))
		self.myMqttClient.start()

	def end(self):
		# if needed, perform some other actions befor ending the software
		print ("ending %s" % (self.clientID))
		self.myMqttClient.stop()

	def notify(self, topic, txt):
		# manage here your received message. You can perform some error-check here
		# print ("received '%s' under topic '%s'" % (self.messaggio, topic))
		# self.messaggio = txt;
		# self.messaggio = json.loads(self.messaggio);
		# if self.messaggio['Food_Level'] == 'low':
		# 	message = json.dumps({'Comando':'on'});
		# 	self.myMqttClient.myPublish(topic_pub,message);
		# else:
		# 	message = json.dumps({'Comando':'off'});
		# 	self.myMqttClient.myPublish(topic_pub,message);
		self.myclient = Thingspeak_REST();
		if topic == "IOTproject/SmartFood/Food/Bilancia":
			field = 1;
			self.messaggio = txt;
			self.messaggio = json.loads(self.messaggio);
			if self.messaggio['Food_Level'] == 'low':
				dato = 0;
				self.myclient.GETINVOCATION(dato,field);
				print 'Richiesta inviata per la bilancia'
			else:
				dato = 1;
				self.myclient.GETINVOCATION(dato,field);
				print 'Richiesta inviata per la bilancia'
		else:
			self.messaggio = txt;
			self.messaggio = json.loads(self.messaggio);
			if 'Comando' in self.messaggio.keys():
				field = 2;
				if self.messaggio['Comando'] == 'off':
					dato = 0;
					self.myclient.GETINVOCATION(dato,field);
					print 'Richiesta inviata per il comando'
				else:
					dato = 1;
					self.myclient.GETINVOCATION(dato,field);
					print 'Richiesta inviata per il comando'
			else:
				field = 3;
				if self.messaggio['Attuatore'] == 'off':
					dato = 0;
					self.myclient.GETINVOCATION(dato,field);
					print "Richiesta inviata per l'attuatore"
				else:
					dato = 1;
					self.myclient.GETINVOCATION(dato,field);
					print "Richiesta inviata per l'attuatore"
