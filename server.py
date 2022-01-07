from flask import Flask, request, jsonify
from flask import Flask
import json

app = Flask(__name__)
app.debug = True


@app.route('/http/message/', methods=['post'])
def post_http():
    if not request.data:  # 检测是否有数据
        return ('fail')
    params = request.data.decode('utf-8')
    # 获取到POST过来的数据，因为我这里传过来的数据需要转换一下编码。根据晶具体情况而定
    prams = json.loads(params)
    print(prams)
    # 把区获取到的数据转为JSON格式。
    return print(prams) #jsonify(prams)
    # 返回JSON数据。


if __name__ == '__main__':
    app.run(host='10.0.0.4', port=80)
    # 这里指定了地址和端口号。也可以不指定地址填0.0.0.0那么就会使用本机地址ip