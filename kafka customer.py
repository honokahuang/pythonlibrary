from flask import Flask, request, jsonify
import json
from pykafka import KafkaClient


app = Flask(__name__)

@app.route(rule='/', methods=['POST'])
def everything():

    request_body = request.get_json()
    # request_body = json.dumps(request_body)
    info1 = json.loads(request_body)
    print('Request info: ', request_body)
    # 生成响应信
    response_info = {'msg': 'success'}
    print('Response info:', response_info)
    # 将响应信息转换为 JSON 格式
    response_body = jsonify(response_info)
    # 最终对请求进行相应
    producer.produce(str(response_body).encode())
    return response_body

if __name__ == '__main__':
    host_brokers = '192.168.3.24:9092'
    zookeeper_hosts = '192.168.3.24:2181'
    client = KafkaClient(hosts=host_brokers, zookeeper_hosts=zookeeper_hosts)
    topic = client.topics[b"test1"]
    producer = topic.get_producer(sync=False, delivery_reports=True)
    app.run(host='0.0.0.0', port=6000, debug=False)