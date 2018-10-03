from DoSomething_raspberry_smartfood import DoSomething
import time

if __name__ == "__main__":
    controllobilancia = DoSomething("Food_Level_Controller");
    topic_sub = "IOTproject/SmartFood/Food/Bilancia";
    controllobilancia.run();
    time.sleep(1)
    controllobilancia.myMqttClient.mySubscribe(topic_sub);

    a = 1
    while (a > 0):
        pass;
