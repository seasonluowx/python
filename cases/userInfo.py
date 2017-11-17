import requests

from resources import testconfig
from util import datetimeUtil, authorizationUtil

server_sns = testconfig.configs['server_sns']


def ants_get_user_info(userId, key_word):
    url = server_sns + '/user/' + str(userId) + '?v=v3.2'
    userInfo_result = requests.get(url).json()
    if userInfo_result["code"] != 1:
        return userInfo_result
    return userInfo_result["result"][key_word]


def ants_fllowList(userId, status):
    url = server_sns + '/user/' + str(userId) + '/follows?v=v3.2'
    userInfo_result = requests.get(url).json()
    gmttime=datetimeUtil.get_GMT_time()
    auth=authorizationUtil.get_author("get",url,gmttime,userId,server_sns)
    headers = {'X-Xiaoyi-Date': gmttime,
               'Authorization': auth,
               'Content-Type': 'application/x-www-form-urlencoded'}
    result_follows_list = isFollows(method, url, userId, status, pid, self.server)
    # self.write_str(str(result_follows_list))
    return result_follows_list


def isFollows(self, method, url, userId, status, pid, server):
    try:
        ax = []
        ax.append('userId')
        ax.append('status')
        ax.append('name')
        ax.append('icon')
        # 1 : 表示数组为分析对象
        key_value = self.get_header_fuc_dict(method, url, 'items', ax, pid, server, 'code')
        if key_value != -100 and key_value != -1:
            for i in range(len(key_value)):
                person = key_value[i]['userId']
                status_value = key_value[i]['status']
                if person == userId and status_value == status:
                    return key_value[i]
            return False
        else:
            return key_value
    except Exception as e:
        e.print_exc()
        return -100
