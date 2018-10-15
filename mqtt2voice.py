#!python


# speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav

import subprocess, math, struct, re

import paho.mqtt.client
mqttbroker = "mqtt.local"   # set to None to disable
mqtttopicspeak = "vocopi/say/#"
mqttclient = None


acmd = "aplay -q -t raw -D default -c 1 -f S16_LE -r 8000".split()
blipdurationcycles = 380
blipvolume = 3400
def blipseq(lf):
    if len(lf):
        aplay = subprocess.Popen(acmd, stdin=subprocess.PIPE)
        for f in lf:
            for i in range(blipdurationcycles):
                e = min(i*16/blipdurationcycles, (blipdurationcycles-i)*16/blipdurationcycles, 1)*blipvolume # (does fade in and fade out)
                aplay.stdin.write(struct.pack("<h", int(e*math.sin(i*f/100))))  # some uncalibrated frequency
        aplay.stdin.close()
        aplay.wait()


def blipsay(text, voice="slt"):
    if type(text) == bytes:
        text = text.decode()
    m = re.match('[\d\s,]*', text)
    blips = list(map(int, re.findall('\d+', m.group())))
    words = text[m.end():]
    
    blipseq(blips)

    fcmd = [ 'flite', '-voice', voice ]
    sflite = subprocess.Popen(fcmd, stdin=subprocess.PIPE)
    sflite.stdin.write(words.encode())
    sflite.stdin.close()
    sflite.wait()

    blipseq(list(reversed(blips)))


mqttclient = paho.mqtt.client.Client(mqttbroker)   # global object
def on_connect(client, userdata, flags, rc):
    print("on_connect", client, userdata, flags, rc)
    blipsay("20,50,90 M Q T T Connected")
def on_disconnect(client, userdata, rc):
    print("on_disconnect", client, userdata, rc)
    blipsay("20,50,90 M Q T T Disconnected")
def on_publish(client, userdata, mid):
    print("on_publish", client, userdata, mid)
def on_message(client, userdata, message):
    print("on_message", client, message, message.topic, message.payload)
    voice = {"1":"rms", "2":"kal", "3":"awb"}.get(message.topic[-1], "slt")
    blipsay(message.payload, voice)

mqttclient.on_connect = on_connect
mqttclient.on_publish = on_publish
mqttclient.on_disconnect = on_disconnect
mqttclient.on_message = on_message

print("made and attempting to connect", mqttclient)
mqttclient.connect(mqttbroker)
mqttclient.subscribe(mqtttopicspeak)
mqttclient.loop_forever()




#fsay("Hi there")
#fsay("This is flite speaking")



#shortjblips(12,40)






