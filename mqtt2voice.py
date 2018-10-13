#!python


# speaker-test -c2 --test=wav -w /usr/share/sounds/alsa/Front_Center.wav

import subprocess, math, struct

import paho.mqtt.client
mqttbroker = "mqtt.local"   # set to None to disable
mqttspoken = "vocopi/spoken"
mqtttohear = "vocopi/tohear"
mqttclient = None
spokenhistory = [ "nothing" ]
heardhistory = [ "nothing" ]


# can't get these to work
def shortjblips(n, *lf):
    if len(lf) == 0:
        return
    cmd = [ 'aplay', '-q', '-t', 'raw', '-D', 'default', '-c', '1', '-f', 's8', '-r', '8000' ]
    aplay = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    
    for f in lf:
        for i in range(n):
            e = min(i*16/n, (n-i)*16/n, 1)
            aplay.stdin.write(struct.pack("b", int(e*math.sin(i*f)*127)))
    
    aplay.stdin.close()
    aplay.wait()


def blipsay(text):
    if type(text) == bytes:
        text = text.decode()
    m = re.match('[\d\s,]*', text)
    blips = [int(x)/100  for x in re.findall('\d+', m.group())]
    text = text[m.end():]
    audio.shortjblips(400, *blips)
    tts.say(Dplayer, text, eq_filter, "en-US")
    audio.shortjblips(400, *reversed(blips))

def fsay(words, voice="slt"):  # flite -lv -> kal awb_time kal16 awb rms slt
    cmd = [ 'flite', '-voice', voice ]
    sflite = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    if isinstance(words, str):
        words = words.encode()
    sflite.stdin.write(words)
    sflite.stdin.close()
    sflite.wait()


mqttclient = paho.mqtt.client.Client(mqttbroker)   # global object
def on_connect(client, userdata, flags, rc):
    print("on_connect", client, userdata, flags, rc)
    fsay("M Q T T Connected")
def on_disconnect(client, userdata, rc):
    print("on_disconnect", client, userdata, rc)
    fsay("M Q T T Disconnected")
def on_publish(client, userdata, mid):
    print("on_publish", client, userdata, mid)
def on_message(client, userdata, message):
    print("on_message", client, message, message.topic, message.payload)
    heardhistory.append(message.payload.decode())
    fsay(message.payload)
mqttclient.on_connect = on_connect
mqttclient.on_publish = on_publish
mqttclient.on_disconnect = on_disconnect
mqttclient.on_message = on_message
print("made and attempting to connect", mqttclient)
mqttclient.connect(mqttbroker)
mqttclient.subscribe(mqtttohear)
mqttclient.loop_forever()



fsay("Hi there")
fsay("This is flite speaking")



#shortjblips(12,40)






