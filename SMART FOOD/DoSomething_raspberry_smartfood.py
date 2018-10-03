from MyMQTT import MyMQTT
import json

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
		topic_pub = 'IOTproject/SmartFood/Food/Attuatore';
		self.messaggio = txt;
		self.messaggio = json.loads(self.messaggio);
		if self.messaggio['Food_Level'] == 'low':
			message = json.dumps({'Comando':'on'});
			self.myMqttClient.myPublish(topic_pub,message);
		else:
			message = json.dumps({'Comando':'off'});
			self.myMqttClient.myPublish(topic_pub,message);
