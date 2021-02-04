import csv
import datetime
import json
import request
import serial
import pandas as pd
import redis
import pymongo


pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)


# myclient = pymongo.MongoClient("mongodb://localhost:27017/")
# mydb = myclient["test11"]
# mycol = mydb["test11"]
ser = serial.Serial('/dev/cu.usbmodem14D24401', 9600, timeout=1)
# f = open('date.csv','w',encoding='utf-8')
# csv_writer = csv.writer(f)
# csv_writer.writerow(["Time","Date"])
jsonlist=[]
jsonlist1=[]
list=[]
if ser.is_open:
    try:
        while 1:
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # for date in range(0,8):
            response = ser.readline().decode().strip()
            if response:
                jsonlist.append(response)
                if len(jsonlist) == 2:
                    z={jsonlist[0]:jsonlist[1]}
                    jsonlist1.append(z)
                    # r.set(z)
                    jsonlist.clear()
            if len(jsonlist1) == 8:
                jsonlist1.insert(0,{"Time":now_time})
                jd=json.dumps(jsonlist1)
                print(jd)
                jsonlist1.clear()
                r.lpush("test",jd)


            # print(now_time, list2)
            # if response:
            #     print(now_time,list2)
                # csv_writer.writerow([now_time, response])
                # jsonlist.append(now_time)
                # jsonlist.append(response)
                # templist=json.dumps(jsonlist)

    except KeyboardInterrupt:
        #req=request.POST(url,templist)
        #print(req.text)
        ser.close()
        # f.close()
