# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/3/22

import os
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0]
# scriptpath=os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile

class videoList(Common):
	def __init__(self,server,serve_yy, moduleName):
		Common.__init__(self,server,serve_yy, moduleName)

	def runCase(self,persons):
		isRunClub = False
		isRun = False

		userId=self.get_pid()
		pid=int(userId)
		
		#发现列表==========1.0.1——1.2===================
		index_result = self.ants_find(pid)
		# print(index_result
		nums={}
		for x in index_result:
			if index_result.count(x)>2:
				nums[x]=index_result.count(x)

		if nums != {}:
			self.write_str("1.0.9  发现列表中，前一百条数据中出现次数大于3次的媒体："+str(nums))
			self.write_email_log("1.0.9  ","发现列表中，前一百条数据中出现次数大于3次的媒体："+str(nums),"fail")
		else:
			self.write_str("1.0.9  发现列表媒体展示正常 success")
			self.write_email_log("1.0.9 ","发现列表媒体展示正常","success")
		
		# print("媒体"+str(x)+"重复"+str(nums[x])+"次"


		#结束测试
		self.close_fd()
		self.EndTest()		

def  main():
	reload(sys)
	sys.setdefaultencoding='utf-8'
	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case = videoList(server,serve_yy,'eight')
	case.runCase(persons)

if __name__ == '__main__':
	main()