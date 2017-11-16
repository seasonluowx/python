import json
from urllib import request
import requests

firmware_download_url = "http://localhost:8088/firmware/download?v=v1.0&hw=11&local=en&prodId=8&sn=Z18123&lang=zh-cn&fileType=gzip&projectId=flight"

#通过urllib来请求
# req = request.Request(firmware_download_url)
# content = request.urlopen(req).read();
# print(content.decode('utf-8'))

# requests更加简单
r = requests.get(firmware_download_url);
print("status_code:%s \ncontent:%s \n" %(r.status_code,r.json()))

#定制header,POST发送json数据
get_sessionId_url = "http://localhost:8032/web/operator/login?v=v1.0"
headers={"Content-Type":"application/json"}
datas={"rememberMe": True, "userName": "test", "userPassword": "1234576"}
r2 = requests.post(get_sessionId_url,headers=headers,data=json.dumps(datas))
print("status_code:%s \ncontent:%s \nencoding:%s" %(r2.status_code,r2.json(),r2.encoding))

