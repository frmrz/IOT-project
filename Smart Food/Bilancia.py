from DoSomething_raspberry_smartfood import DoSomething
import time
import json

if __name__ == "__main__":
    bilancia = DoSomething('MyLoadCell');
    topic = 'IOTproject/SmartFood/Food/Bilancia';
    bilancia.run();
    time.sleep(1);

    while 1>0:
        a = 0;
        while (a < 30):
            message = json.dumps({"Food_Level":"ok"});
            bilancia.myMqttClient.myPublish(topic,message);
            a = a+1;
            time.sleep(1);
        message = json.dumps({"Food_Level":"low"});
        bilancia.myMqttClient.myPublish(topic,message);
        time.sleep(1);
