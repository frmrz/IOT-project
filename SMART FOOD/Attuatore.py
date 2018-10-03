from DoSomething_actuator_smartfood import DoSomething
import time

if __name__ == "__main__":
    attuatore = DoSomething("Actuator");
    topic_sub = "IOTproject/SmartFood/Food/Attuatore";
    attuatore.run();
    time.sleep(1)
    attuatore.myMqttClient.mySubscribe(topic_sub);

    a = 1
    while (a > 0):
        pass;
