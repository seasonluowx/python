# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/5/17
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0]
# scriptpath=os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile


class Login(Common):
	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)

	def runCase(self,persons):

		mediaId = self.get_mediaId()
		print('mediaId:'+str(mediaId))
		mediaId = int(mediaId)

		userId=self.get_pid()
		pid=int(userId)

		#话题投诉==========1.0.11-1===================
		bodys={}
		bodys['comment']='投诉媒体'
		bodys['mediaId']=mediaId
		claim = self.ants_claim(bodys,persons[1])
		print(claim)
		if claim ==-1 or claim ==-100:
			self.write_str('1.0.11-1 投诉媒体异常 error')
			self.write_email_log('1.0.11-1','投诉媒体异常','error')
		elif claim =='success':
			self.write_str("1.0.11-1 投诉媒体 success")
			self.write_email_log('1.0.11-1',"投诉媒体","success")	
		else:
			self.write_str("1.0.11-1 投诉媒体 fail")
			self.write_email_log('1.0.11-1',"投诉媒体","fail")	

		#轮播============1.0.11-2==============
		carouselsUser_time1=self.get_now_time()
		carousels_user = self.ants_carousels('carousel',pid)
		carouselsUser_time2=self.get_now_time()
		print(carousels_user)
		if carousels_user==-1 or carousels_user == -100:
			self.write_str('1.0.11-2 轮播接口异常 error')
			self.write_email_log('1.0.11-2','轮播接口异常','error')
		elif len(carousels_user)>0:
			self.write_str('1.0.11-2 轮播接口carousel获取 success,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)))
			self.write_email_log('1.0.11-2','轮播接口carousel获取,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)),'success')
		else:
			self.write_str('1.0.11-2 轮播接口carousel获取 fail')
			self.write_email_log('1.0.11-2','轮播接口carousel获取','fail')

		#热门标签============1.0.11-2==============
		carouselsUser_time1=self.get_now_time()
		carousels_user = self.ants_carousels('tagCategory',pid)
		carouselsUser_time2=self.get_now_time()
		print(carousels_user)
		if carousels_user==-1 or carousels_user == -100:
			self.write_str('1.0.11-2 轮播接口异常 error')
			self.write_email_log('1.0.11-2','轮播接口异常','error')
		elif len(carousels_user)>0:
			self.write_str('1.0.11-2 轮播接口tagCategory获取 success,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)))
			self.write_email_log('1.0.11-2','轮播接口tagCategory获取,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)),'success')

			for x in range(len(carousels_user)):
				tagId=carousels_user[x]['id']
				print('tagId:'+str(tagId))

				#标签最热列表
				city_time1=self.get_now_time()
				tags_hot = self.ants_tags_hot(tagId,pid)
				print(tags_hot)
				city_time2=self.get_now_time()
				if tags_hot == -1 or tags_hot == -100:
					self.write_str('1.0.11-3 标签'+str(tagId)+'最热列表异常 error')
					self.write_email_log('1.0.11-3',"标签"+str(tagId)+"用户列表异常","error")
				elif len(tags_hot)>0:
					self.write_str('1.0.11-3 标签'+str(tagId)+'最热列表 success，耗时'+str(self.get_time_long(city_time1,city_time2)))
					self.write_email_log('1.0.11-3',"标签"+str(tagId)+"最热列表，耗时"+str(self.get_time_long(city_time1,city_time2)),"success")
				else:
					self.write_str('1.0.11-3 标签'+str(tagId)+'最热列表为空 fail')
					self.write_email_log('1.0.11-3',"标签"+str(tagId)+"最热列表为空","fail")

		else:
			self.write_str('1.0.11-2 轮播接口tagCategory获取 fail')
			self.write_email_log('1.0.11-2','轮播接口tagCategory获取','fail')

		#闪屏============1.0.11-2==============
		carouselsUser_time1=self.get_now_time()
		carousels_user = self.ants_screen(pid)
		carouselsUser_time2=self.get_now_time()
		print(carousels_user)
		if carousels_user==-1 or carousels_user == -100:
			self.write_str('1.0.11-4 splash_screen信息列表异常 error')
			self.write_email_log('1.0.11-4 ','splash_screen信息列表异常','error')
		elif len(carousels_user)>0:
			self.write_str('1.0.11-4 splash_screen信息列表 success,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)))
			self.write_email_log('1.0.11-4','splash_screen信息列表,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)),'success')
		else:
			self.write_str('1.0.11-4 splash_screen信息列表 fail')
			self.write_email_log('1.0.11-4','splash_screen信息列表','fail')

		# 媒体详情==========1.0.1——1.1 ===================
		detail_time1 = self.get_now_time();
		mediaInfoResult_init = self.ants_media_detail(mediaId,pid)
		print(mediaInfoResult_init)
		detail_time2 = self.get_now_time();
		if mediaInfoResult_init ==-1 or mediaInfoResult_init ==-100:
			self.write_str(u"1.0.11-5 媒体详情异常 error")
			self.write_email_log('1.0.11-5',"媒体详情异常,耗时"+str(self.get_time_long(detail_time1,detail_time2)),"error")
		else:
			visits_init =mediaInfoResult_init[0]['visits'] 
			
			#更新媒体浏览数
			updateVisit_result=self.ants_update_visit(mediaId,pid)
			print(updateVisit_result)
			if updateVisit_result == 'success':
				self.write_str(u"1.0.11-6 数据浏览visit更新 success")
				self.write_email_log('1.0.11-6',"数据浏览visit更新","success")

				#获取媒体详情
				mediaInfoResult = self.ants_media_detail(mediaId,pid)
				if mediaInfoResult ==-1 or mediaInfoResult ==-100:
					self.write_str(u"1.0.11-5 媒体详情异常 error")
					self.write_email_log('1.0.11-5',"媒体详情异常",'error')
				else:
					visits = mediaInfoResult[0]['visits']
					print(visits)
					print(visits_init)
					if visits == visits_init+2:
						self.write_str(u"1.0.11-7 修改媒体浏览数后,媒体详情visit更新 success")
						self.write_email_log('1.0.11-7',"修改媒体浏览数后,媒体详情visit更新","success")
					else:
						self.write_str("1.0.11-7 修改媒体浏览数后,媒体详情visit更新 fail")
						self.write_email_log('1.0.11-7','修改媒体浏览数后,媒体详情visit更新','fail')
			else:
				self.write_str(u"1.0.11-6 数据浏览visit更新 fail")
				self.write_email_log('1.0.11-6',"数据浏览visit更新","fail")



def main():
	reload(sys)

	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=Login(server,serve_yy,'eleven')
	case.runCase(persons)

if __name__ == '__main__':
	main()