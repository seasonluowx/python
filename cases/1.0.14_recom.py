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


class Recom(Common):

	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)

	def runRecomCase(self,persons):
		runTag=False
		RunCase=False

		result = self.get_mediaId()
		mediaId = int(result)
		print(mediaId)

		userId=self.get_pid()
		pid=int(userId)

		if mediaId != 0:
			RunCase =True
			
		if RunCase:
			self.write_str('=======推荐标示的识别操作=============')
			self.write_email_log('0000','=======推荐标示的识别操作=============','success')

			#后台web系统推荐或取消推荐媒体
			bodys={}
			bodys['mediaId']=mediaId
			bodys['type']=1 #1-推荐 0-取消推荐或取消差评,-1差评
			cachesync = self.ants_cachesync(bodys,'1')
			if cachesync =='success':
				self.write_str(u"1.0.14-1 后台系统推荐媒体"+str(mediaId)+" success")
				self.write_email_log("1.0.14-1 ","后台系统推荐媒体"+str(mediaId),"success")

				# 发布影响首页列表==========1.0.1——1.2===================
				index_time1 =self.get_now_time()
				index_isRecomm = self.ants_index('mediaId',mediaId,'ranking',pid)
				print(index_isRecomm)
				index_time2=self.get_now_time()
				if index_isRecomm==[1]:
					self.write_str(u"1.0.14-2 首页推荐列表ranking展示 success，耗时"+str(self.get_time_long(index_time1,index_time2)))
					self.write_email_log(u"1.0.14-2 ","首页推荐列表ranking展示,耗时"+str(self.get_time_long(index_time1,index_time2)),"success")
				else:
					self.write_str('1.0.14-2 首页推荐列表ranking展示 fail')
					self.write_email_log('1.0.14-2 ","首页推荐列表ranking展示','fail')

				# 发布影响媒体详情==========1.0.1——1.1 ===================
				detail_time1 = self.get_now_time();
				mediaInfoResult = self.ants_media_detail(mediaId,pid)
				print(mediaInfoResult)
				detail_time2 = self.get_now_time();
				if mediaInfoResult ==-1 or mediaInfoResult ==-100:
					self.write_str(u"1.0.14-3 媒体详情内ranking展示异常 error")
					self.write_email_log(u"1.0.14-3 ","媒体详情内ranking展示异常,耗时"+str(self.get_time_long(detail_time1,detail_time2)),"error")
				elif mediaInfoResult[0]['ranking']==1:
					self.write_str(u"1.0.14-3 媒体详情内ranking展示 success")
					self.write_email_log(u"1.0.14-3 ","媒体详情内ranking展示,耗时"+str(self.get_time_long(detail_time1,detail_time2)),"success")

					tagId=mediaInfoResult[0]['tagList'][0]['id']
					runTag = True
					print(tagId)

					tag_mediaId_isRecomm = self.ants_tags_least(tagId,'mediaId',mediaId,'ranking',pid)
					print(tag_mediaId_isRecomm)
					if tag_mediaId_isRecomm==[1]:
						self.write_str("1.0.14-4 标签最新列表ranking展示 success")
						self.write_email_log("1.0.14-4 ","标签最新列表ranking展示","success")
					else:
						self.write_str("1.0.14-4 标签最新列表ranking展示 fail")
						self.write_email_log("1.0.14-4 ","标签最新列表ranking展示 fail")

				else:
					self.write_str(u"1.0.14-3 媒体详情内ranking展示 fail")
					self.write_email_log(u"1.0.14-3 ","媒体详情内ranking展示,耗时"+str(self.get_time_long(detail_time1,detail_time2)),"fail")

			else:
				self.write_str(u"1.0.14-1 后台系统推荐媒体 fail")
				self.write_email_log("1.0.14-1 ","后台系统推荐媒体","fail")

			#视频列表
			index_result = self.ants_video_index('ranking',0,'mediaId',pid)
			print(index_result)
			if index_result ==-1 or index_result ==-100:
				self.write_str(u"1.0.14-5 媒体列表展示异常 error")
				self.write_email_log("1.0.14-5 ","媒体列表展示异常","error")
			elif index_result ==False:
				self.write_str(u"1.0.14-5 媒体列表内都为推荐媒体 fail")
				self.write_email_log("1.0.14-5 ","媒体列表内都为推荐媒体","fail")
			else:
				#设置
				bodys['mediaId']=index_result[0]
				bodys['type']=1 #1-推荐 0-取消推荐
				cachesync = self.ants_cachesync(bodys,'1')
				if cachesync =='success':
					self.write_str(u"1.0.14-6 后台系统推荐媒体"+str(index_result)+" success")
					self.write_email_log("1.0.14-6 ","后台系统推荐媒体"+str(index_result),"success")

					##视频列表
					isRecomm_vlist = self.ants_video_index('mediaId',index_result[0],'ranking',pid)
					if isRecomm_vlist ==[1]:
						self.write_str(u"1.0.14-7 视频列表ranking展示 success")
						self.write_email_log("1.0.14-7 ","视频列表ranking展示","success")
					else:
						self.write_str(u"1.0.14-7 视频列表ranking展示 success")
						self.write_email_log("1.0.14-7 ","视频列表ranking展示","success")

					#取消推荐
					bodys['type']=0 #1-推荐 0-取消推荐
					cachesync = self.ants_cachesync(bodys,'1')
				else:
					self.write_str(u"1.0.14-6 后台系统推荐媒体"+str(index_result)+" fail")
					self.write_email_log("1.0.14-6 ","后台系统推荐媒体"+str(index_result),"fail")

			#发现列表
			find_result = self.ants_find_new('ranking',0,'mediaId',pid,0)
			print(find_result)
			if find_result ==-1 or find_result ==-100:
				self.write_str(u"1.0.14-8 发现列表展示异常 error")
				self.write_email_log("1.0.14-8 ","发现列表展示异常","error")
			elif find_result ==False:
				self.write_str(u"1.0.14-8 发现列表内都为推荐媒体 fail")
				self.write_email_log("1.0.14-8 ","发现列表内都为推荐媒体","fail")
			else:
				#设置
				bodys['mediaId']=find_result[0]
				bodys['type']=1 #1-推荐 0-取消推荐
				cachesync = self.ants_cachesync(bodys,'1')
				if cachesync =='success':
					self.write_str(u"1.0.14-9 后台系统推荐媒体"+str(find_result[0])+" success")
					self.write_email_log("1.0.14-9 ","后台系统推荐媒体"+str(find_result[0]),"success")

					isRecomm=False
					for x in range(0,10):
						#发现列表
						isRecomm_find = self.ants_find_new('mediaId',find_result[0],'ranking',pid,x)
						print(isRecomm_find)
						if isRecomm_find == False:
							continue
						elif isRecomm_find == [1]:
							isRecomm=True
							break

					if isRecomm == True:
						self.write_str(u"1.0.14-10 发现列表ranking展示 success")
						self.write_email_log("1.0.14-10 ","发现列表ranking展示","success")
					else:
						self.write_str(u"1.0.14-10 发现列表ranking展示 fail")
						self.write_email_log("1.0.14-10 ","发现列表ranking展示","fail")

					#取消推荐
					bodys['type']=0 #1-推荐 0-取消推荐
					cachesync = self.ants_cachesync(bodys,'1')
				else:
					self.write_str(u"1.0.14-9 后台系统推荐媒体"+str(find_result[0])+" fail")
					self.write_email_log("1.0.14-9 ","后台系统推荐媒体"+str(find_result[0]),"fail")

			#设置差评
			bodys={}
			bodys['mediaId']=mediaId
			bodys['type']=-1 #1-推荐 0-取消推荐或取消差评,-1差评
			cachesync = self.ants_cachesync(bodys,'1')
			if cachesync =='success':
				self.write_str(u"1.0.14-11 后台系统推荐媒体"+str(mediaId)+" success")
				self.write_email_log("1.0.14-11 ","后台系统推荐媒体"+str(mediaId),"success")

				#首页
				index_isRecomm2 = self.ants_index('mediaId',mediaId,'ranking',pid)
				if index_isRecomm2==[-1]:
					self.write_str(u"1.0.14-12 首页推荐列表ranking差评展示 success")
					self.write_email_log(u"1.0.14-12 ","首页推荐列表ranking差评展示","success")
				else:
					self.write_str('1.0.14-12 首页推荐列表ranking差评展示 fail')
					self.write_email_log('1.0.14-12 ','首页推荐列表ranking差评展示','fail')

				#媒体详情
				mediaInfoResult2 = self.ants_media_detail(mediaId,pid)
				if mediaInfoResult2 ==-1 or mediaInfoResult2 ==-100:
					self.write_str(u"1.0.14-13 媒体详情内ranking差评后展示异常 error")
					self.write_email_log(u"1.0.14-13 ","媒体详情内ranking差评后展示异常 error")
				elif mediaInfoResult2[0]['ranking']==-1:
					self.write_str(u"1.0.14-13 媒体详情内ranking差评后展示 success")
					self.write_email_log(u"1.0.14-13 ","媒体详情内ranking差评后展示","success")

			#发现列表---设置差评
			find_result2 = self.ants_find_new('ranking',0,'mediaId',pid,0)
			print(find_result2)
			if find_result2 ==-1 or find_result2 ==-100:
				self.write_str(u"1.0.14-14 发现列表展示异常 error")
				self.write_email_log("1.0.14-14 ","发现列表展示异常","error")
			elif find_result2 ==False:
				self.write_str(u"1.0.14-14 发现列表内都为推荐媒体 fail")
				self.write_email_log("1.0.14-14 ","发现列表内都为推荐媒体","fail")
			else:
				#设置
				bodys['mediaId']=find_result2[0]
				bodys['type']=-1 #1-推荐 0-取消推荐或取消差评,-1差评
				cachesync = self.ants_cachesync(bodys,'1')
				if cachesync =='success':
					self.write_str(u"1.0.14-15 后台系统差评媒体"+str(find_result2[0])+" success")
					self.write_email_log("1.0.14-15 ","后台系统差评媒体"+str(find_result2[0]),"success")

					#发现媒体
					isRecomm2=False
					for x in range(0,10):
						#发现列表
						isRecomm_find2 = self.ants_find_new('mediaId',find_result2[0],'ranking',pid,x)
						print(isRecomm_find2)
						if isRecomm_find2 == False:
							continue
						else:
							isRecomm2=True
							break

					if isRecomm2 != True:
						self.write_str(u"1.0.14-16 差评媒体,发现列表不展示 success")
						self.write_email_log("1.0.14-16 ","差评媒体,发现列表不展示","success")
					else:
						self.write_str(u"1.0.14-16 差评媒体,发现列表不展示 fail")
						self.write_email_log("1.0.14-16 ","差评媒体,发现列表不展示","fail")


					#取消差评
					bodys['type']=0 #1-推荐 0-取消推荐
					cachesync = self.ants_cachesync(bodys,'1')
				else:
					self.write_str(u"1.0.14-15 后台系统推荐媒体"+str(find_result2[0])+" fail")
					self.write_email_log("1.0.14-15 ","后台系统推荐媒体"+str(find_result2[0]),"fail")



def main():
	reload(sys)


	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=Recom(server,serve_yy,'forteen')
	case.runRecomCase(persons)

if __name__ == '__main__':
	main()