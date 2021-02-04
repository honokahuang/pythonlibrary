import redis
from flask import Flask, request, jsonify
import json
from pykafka import KafkaClient


app = Flask(__name__)

@app.route(rule='/', methods=['POST'])
def everything():

    request_body = request.get_json()
    response_info = {'msg': 'success'}
    print('Response info:', response_info)
    response_body = str(jsonify(response_info))
    producer.produce(response_body.encode())
    r.lpush("test", response_body)
    return response_body

if __name__ == '__main__':
    host_brokers = '192.168.3.24:9092'
    zookeeper_hosts = '192.168.3.24:2181'
    client = KafkaClient(hosts=host_brokers, zookeeper_hosts=zookeeper_hosts)
    topic = client.topics[b"test1"]
    producer = topic.get_producer(sync=False, delivery_reports=True)
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    app.run(host='0.0.0.0', port=6000, debug=False)