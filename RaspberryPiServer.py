from flask import Flask, request, jsonify
import json

# 创建一个服务
app = Flask(__name__)
# 创建一个接口 指定路由和请求方法 定义处理请求的函数
@app.route(rule='/', methods=['POST'])
def everything():
    # 获取 JSON 格式的请求体 并解析
    request_body = request.get_json()
    info1 = json.loads(request_body)
    print(info1[0]['Time'])
    # print('Request info: ', request_body)
    # 生成响应信
    response_info = 'success'
    # print('Response info:', response_info)
    # 将响应信息转换为 JSON 格式
    response_body = jsonify(response_info)
    # 最终对请求进行相应
    return response_body

if __name__ == '__main__':
    # 启动服务 指定主机和端口
    app.run(host='0.0.0.0', port=6000, debug=False)