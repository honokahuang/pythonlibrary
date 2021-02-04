from pykafka import KafkaClient
import datetime
import time
import json
#生产者
# 可接受多个client
# host_brokers = '192.168.3.55:9092,192.168.3.58:9092,192.168.3.59:9092,192.168.3.27:9092,192.168.3.15:9092'
# # 如果有chroot path 就放到端口号后面/kfk1
# zookeeper_hosts = '192.168.3.55:2181,192.168.3.58:2181,192.168.3.59:2181,192.168.3.27:2181,192.168.3.15:2181'
totalUseTime=0.0
host_brokers = '192.168.3.24:9092'
# 如果有chroot path 就放到端口号后面/kfk1
zookeeper_hosts = '192.168.3.24:2181'
a=1000
client = KafkaClient(hosts=host_brokers,zookeeper_hosts=zookeeper_hosts)
topic = client.topics[b"test1"]
# 将产生kafka同步消息，这个调用仅仅在我们已经确认消息已经发送到集群之后
# with topic.get_sync_producer() as producer:
#     for i in range(100):
#         producer.produce(('honoka test message ' + str(i ** 2)).encode())
producer = topic.get_producer(sync=False, delivery_reports=True)
for i in range(a):
    startTime = time.time()
    now_time = datetime.datetime.now().strftime('%H:%M:%S')
    producer.produce(now_time.encode())
    endTime = time.time()
    useTime = (endTime - startTime) * 1000
    totalUseTime = totalUseTime + useTime
    if i == a-1:
        end='end'
        producer.produce((end).encode())

avgUseTime=totalUseTime/int(a)
print("Average rtt:"+str(avgUseTime)+"ms")