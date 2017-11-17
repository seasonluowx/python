import base64
import hashlib
import hmac
import random
import sys
import traceback
from urllib import request

from util import fileUtil

def get_author(method,url, gttime, pid, server):
    try:
        author = get_right_auth(method, url, gttime, pid, server)
        author = author.replace('\n', '')
        return author
    except Exception as e:
        traceback.print_exc()


def get_right_auth(self, method, url, gttime, pid, server):
    token, tokenSecret = self.get_token_info(pid, self.server)
    uri = self.get_uri_querystring(url, server)
    authorization = get_signature(token, tokenSecret, method, uri, gttime)
    return authorization


def get_token_info(self, pid, server):
    url = server + "/pid/token?v=v3.2&pid=" + str(pid)
    content = self.get(url)
    result = self.get_release_result(eval(content))
    token = result['token']
    tokenSecret = result['tokenSecret']
    return token, tokenSecret


# Method GET
def get(self, url):
    response = request.urlopen(url)
    content = response.read()
    return content


def get_release_result(self, dc={}):
    for key in dc:
        if key == "result":
            result = dc['result']
            return result
    return "wrong token ................"


def get_uri_querystring(self, url, server):
    uri = ""
    index = url.find(server)
    keystr = url[index + len(server):]
    indx = keystr.find('?')
    if indx == -1:
        uri = keystr
    else:
        uri = keystr[:indx]
        # print(uri
    return uri


# 加密token
def get_signature(self, token, tokenSecret, method, uri, gttime):
    signature = self.set_signature(method, uri, tokenSecret, gttime)
    print('signature:' + str(signature) + ',token:' + str(token))
    ss = "token=" + str(token) + "&signature=" + str(signature)
    authorization = base64.encodebytes(ss)
    fileUtil.writeAuth(authorization + '\n')
    return authorization


# 制作签名
def set_signature(self, requestMethod, requestURI, tokenSecret, gttime):
    XIAOYI_DATE = gttime
    fileUtil.writeAuth(XIAOYI_DATE + '\n')
    signStr = XIAOYI_DATE + requestMethod + requestURI
    signature = self.hmac_sha1(tokenSecret, signStr)
    return signature


# 加密方法
def hmac_sha1(self, tokenSecret, datas):
    ts = tokenSecret.encode('utf-8')
    dt = datas.encode('utf-8')
    reString = base64.b64encode(hmac.new(ts, dt, digestmod=hashlib.sha1).digest())
    return reString

def get_random():
    sn = ''
    for i in range(5):
        rn = random.randint(0, 9)
        sn = sn + str(rn)
    return sn
