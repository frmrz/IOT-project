from DoSomething_raspberry_TSadaptor import DoSomething
import time

if __name__ == "__main__":
    TSadaptor_PS = DoSomething("Thingspeak_Adaptor");
    topic_sub = "IOTproject/SmartFood/Food/#";
    TSadaptor_PS.run();
    time.sleep(1)
    TSadaptor_PS.myMqttClient.mySubscribe(topic_sub);

    a = 1
    while (a > 0):
        pass;
