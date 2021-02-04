import csv
import datetime
import json
import serial
import redis
import requests
import serial.tools.list_ports
from time import sleep
from NeuroPy import NeuroPy

#function
def FindSerialDevice(name):
    port_list = list(serial.tools.list_ports.comports())
    for p in port_list:
        print(p.device)
    i = input(name)
    port = port_list[int(i) - 1]
    print(port[0])
    return port[0]

def PostRequest(request_body):
    # 构造服务接口地址
    url = 'http://localhost:{0}/'.format(6000)
    r0 = requests.post(url=url, json=request_body)
    # print(r0.json())


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)

serport = FindSerialDevice("Select the Serial port: ")
ser = serial.Serial(serport, 9600, timeout=1)
mindwaveport = FindSerialDevice("Select the Mindwave port: ")
bluetooth_baund_rate = input('bluetooth baund rate (default: 57600) >') or 57600
mindwave = NeuroPy(mindwaveport, bluetooth_baund_rate)
jsonlist = []
jsonlist1 = []
list = []

if ser.is_open:
    ser.flushOutput()
    ser.flushInput()
    try:
        mindwave.start()

        while 1:
            ser.flushOutput()
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            response = ser.readline().decode().strip()
            low_alpha = mindwave.low_alpha
            high_alpha = mindwave.high_alpha
            low_beta = mindwave.low_beta
            high_beta = mindwave.high_beta
            meditation = mindwave.meditation
            if response:
                jsonlist.append(response)
                if len(jsonlist) == 2:
                    z = {jsonlist[0]: jsonlist[1]}
                    jsonlist1.append(z)
                    jsonlist.clear()
            if len(jsonlist1) == 8:
                jsonlist1.insert(0, {"Time": now_time})
                jsonlist1.append({"low_alpha": low_alpha})
                jsonlist1.append({"high_alpha": high_alpha})
                jsonlist1.append({"low_beta": low_beta})
                jsonlist1.append({"high_beta": high_beta})
                jsonlist1.append({"meditation": meditation})
                jd = json.dumps(jsonlist1)
                print(jd)
                jsonlist1.clear()
                r.lpush("test", jd)
                PostRequest(jd)
                ser.flushOutput()
                ser.flushInput()
                # pass

    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        mindwave.stop()
        ser.close()
    except Exception as e:
        print(f'fucked {e}')


