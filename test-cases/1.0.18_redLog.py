# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/2/22
import os
import sys
from importlib import reload

import paramiko as paramiko

from Common import Common

crupath = sys.path[0]
# scriptpath=os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile


class readLog(Common):
	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)
		self.fdm = open(os.path.join(crupath,'userId.txt'),'w')

	def runCase(self,persons):
		print('++++++++++++++++')
		#连接服务器
		self.clientService()

		# a=0
		# #读取文件
		# fd = open('D:\\log\\log.txt','rb')
		# lines = fd.readlines()

		# for line in lines:
		# 	if 'PushMessageCacheService:' in line:
		# 		print(line
		# 		a=a+1
		# print('共发现目标函数PushMessageCacheService '+str(a)+'次'
		# self.write_str('1.0.18 共发现目标函数PushMessageCacheService '+str(a)+'次')
		# self.write_email_log('1.0.18','共发现目标函数PushMessageCacheService '+str(a)+'次','fail')
		# fd.close()
	
	def clientService(self):

		global time
		dd = open(os.path.join(crupath,"time.txt"),'rb')
		time_con = dd.readline().strip('\n')
		time_con =time.strptime(time_con,'%Y-%m-%d %H:%M:%S')
		print(type(time_con),time_con)
		print('*************')

		b=0
		isOk=True
		client = paramiko.SSHClient()
		client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		client.connect('139.196.234.143', 22, username='root', password='PuZLbXjGo5gVEt33', timeout=4)

		stdin, stdout, stderr = client.exec_command('grep -n PushMessageCacheService: /opt/v3.8/sns-cache/nohup.out')	
		for std in stdout.readlines():
			print(type(std),std)
			con=std[7:26]
			con=time.strptime(con,'%Y-%m-%d %H:%M:%S')
			print('-------start-----------')
			print(type(con),con)
			print('---------end---------')
			if con >= time_con:
				print(std)
				b=b+1
			else:
				isOk=False
		if isOk:
			self.write_str('1.0.18 共发现目标函数PushMessageCacheService '+str(b)+'次')
			self.write_email_log('1.0.18','共发现目标函数PushMessageCacheService '+str(b)+'次','success')
		else:
			self.write_str('1.0.18 未发现目标函数PushMessageCacheService')
			self.write_email_log('1.0.18','未发现目标函数PushMessageCacheService ','fail')

		# stdin, stdout, stderr = client.exec_command('ls -l /opt/v3.8/sns-cache')
		# sftp = client.open_sftp()
		# #sftp.mkdir('abc')#在远端主机创建目录abc
		# sftp.get('/opt/v3.8/sns-rest/nohup.out', r'D:\\log\\log.txt')#下载远端家目录文件到本
		# time.sleep(60)

		client.close()

def main():
	reload(sys)


	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=readLog(server,serve_yy,'eighteen')
	case.runCase(persons)

if __name__ == '__main__':
	main()