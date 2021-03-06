import os
import sys
from datetime import datetime

import requests

from cases import userInfo
from resources import testconfig
from util import datetimeUtil, fileUtil

crupath = sys.path[0]
testCasesPath = os.path.join(crupath, 'cases')

class Login():
	def __init__(self):
		self.server_sns=testconfig.configs['server_sns']

	def runCase(self):
		fdx = ""
		fd_eml = ""
		#=============模拟临时登录======================
		bodys={}
		bodys['mobile']='15555555555'
		bodys['password']='WpTG5VdA+ZDOupjrUYTxa0AgOmjlBssG94CitC5mY+4='

		login_time1=datetime.utcnow()
		userId = self.user_login(bodys)['result']
		login_time2=datetime.utcnow()
		if userId != '' and userId !=[]:
			fdx+='1.1.10-1 用户%s登录 success,耗时%d毫秒\n'%(userId['userId'],datetimeUtil.get_time_long(login_time1,login_time2))
			fd_eml+='1.1.10-1\t\t用户%s登录%d\t\tsuccess\n'%(userId['userId'],datetimeUtil.get_time_long(login_time1,login_time2))
			pid=userId['userId']
			#写入文件
			with open(os.path.join(crupath, 'logs/userId.txt'), 'w', encoding='utf-8-sig') as userIdf:
				userIdf.write(str(pid))
			#查看用户详情
			userInfo_userId = userInfo.ants_get_user_info(pid,'userId')
			if userInfo_userId == pid:
				fdx+='1.1.10-2 用户'+str(pid)+'登录后访问用户详情 success\n'
				fd_eml+='1.1.10-2\t\t用户%d登录后访问用户详情\t\tsuccess\n'%pid
			else:
				fdx+='1.1.10-2 用户'+str(pid)+'登录后访问用户详情 fail\n'
				fd_eml+='1.1.10-2\t\t用户%d登录后访问用户详情\t\tfail\n'%pid
		else:
			fdx+='1.1.10-1 用户'+str(userId)+'登录 fail\n'
			fd_eml+='1.1.10-1\t\t用户%s登录\t\tfail\n'%str(userId)
		fileUtil.writeRecord(fdx)
		fileUtil.writeEmailText(fd_eml)

		return

	def user_login(self, bodys):
		url = self.server_sns + '/user/login_xiaoyi?v=v3.2'
		user_login_result = requests.post(url,data=bodys)
		return user_login_result.json()

def main():
	case=Login()
	case.runCase()

if __name__ == '__main__':
	main()