# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/6/5
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0]
# scriptpath=os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile


class Screen(Common):
	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)

	def runScreenCase(self,persons):
		keys={}
		for x in range(1,10):
			#闪屏============1.0.11-2==============
			carouselsUser_time1=self.get_now_time()
			carousels_user = self.ants_screen(persons[0])
			carouselsUser_time2=self.get_now_time()
			print(carousels_user)
			if carousels_user==-1 or carousels_user == -100:
				self.write_str('1.0.11-4 splash_screen信息列表异常 error')
				self.write_email_log('1.0.11-4','splash_screen信息列表异常','error')
			elif len(carousels_user)>0:
				id=carousels_user[0]['id']
				if keys.has_key(id):
					keys[id]=keys[id]+1
				else:
					keys[id]=1

				print(keys)

		self.write_str('1.0.11-4 splash_screen信息列表内展示id及展示次数'+str(keys.items())+' success,')
		self.write_email_log('1.0.11-4',' splash_screen信息列表','success')

def main():
	reload(sys)


	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=Screen(server,serve_yy,'firteen')
	case.runScreenCase(persons)

if __name__ == '__main__':
	main()