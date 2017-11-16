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
		
		#视频列表==========1.0.1——1.2===================
		index_time1 =self.get_now_time()
		index_result = self.ants_video_index('all','','',pid)
		# print(index_result
		index_time2=self.get_now_time()

		mediaIds_result = [] 
		if index_result ==-1 or index_result ==-100:
			self.write_str('1.0.8-1.1 视频列表异常 error')
			self.write_email_log('1.0.8-1.1 ','视频列表异常','error')
		elif len(index_result)>1:
			for x in range(len(index_result)-1):
				if index_result[x]['mediaType'] != 1:
					self.write_str('1.0.8-1.1 视频列表有非视频媒体 error')
					self.write_email_log('1.0.8-1.1 ','视频列表有非视频媒体','error')

				#mediaId
				mediaIds = index_result[x]['mediaId']
				mediaIds_result.append(mediaIds)
				isRun = True
			if len(mediaIds_result) == len(set(mediaIds_result)):
				self.write_str("1.0.8-1.1 视频列表内视频媒体存在且唯一 success,耗时"+str(self.get_time_long(index_time1,index_time2)))
				self.write_email_log("1.0.8-1.1 ","视频列表内视频媒体存在且唯一,耗时"+str(self.get_time_long(index_time1,index_time2)),"success")
			else:
				self.write_str('1.0.8-1.1 视频列表数据重复 fail')
				self.write_email_log('1.0.8-1.1 ','发视频列表数据重复','fail')	
		else:
			self.write_str("1.0.1-1.1 视频列表为空 fail")
			self.write_email_log("1.0.1-1.1 ","视频列表为空","fail")


		for x in range(0,20):
			print(len(mediaIds_result))
			if not isRun:
				return
			#获取媒体详情
			# print(mediaIds_result[x]
			mediaId =mediaIds_result[x]
			mediaInfoResult = self.ants_media_detail(mediaId,pid)
			print(str(mediaInfoResult)+'======')
			if mediaInfoResult != -1 and mediaInfoResult !=-100:
				userId = mediaInfoResult[0]['userId']
				if userId != pid:

					#评论消息	
					comments_init=mediaInfoResult[0]['comments']
					commentList_init=mediaInfoResult[0]['commentResList']
					#添加评论
					add_time1 =self.get_now_time();
					bodys_cn = {}
					bodys_cn['content'] = self.get_random() + ' === Good !===> '+ self.get_local_time()
					bodys_cn['mediaId'] = mediaId
					add_result = self.ants_add_comment(mediaId,bodys_cn,persons[1])
					print('======'+str(add_result))
					add_time2 =self.get_now_time();
					if add_result == 'success':
						self.write_str("1.0.8-2.1 添加评论成功！耗时"+str(self.get_time_long(add_time1,add_time2)))
						self.write_email_log("1.0.8-2.1 ","添加评论成功！耗时"+str(self.get_time_long(add_time1,add_time2)),'success')

						#h获取媒体列表内的 comments
						vedioIndex_com = self.ants_video_index('mediaId',mediaId,'comments',pid)
						print(type(vedioIndex_com),vedioIndex_com)
						print(type(comments_init),comments_init)
						if vedioIndex_com ==-1 or vedioIndex_com ==-100:
							self.write_str('1.0.8-2.2 添加评论后媒体列表展示异常 error')
							self.write_email_log('1.0.8-2.2 ','添加评论后媒体列表展示异常','error')
						elif vedioIndex_com == False:
							self.write_str('1.0.8-2.2 添加评论后媒体列表内comments+1 fail')
							self.write_email_log('1.0.8-2.2 ','添加评论后媒体列表内comments+1','fail')
						elif vedioIndex_com[0] ==comments_init+1:
							self.write_str('1.0.8-2.2 添加评论后媒体列表内comments+1 success')
							self.write_email_log('1.0.8-2.2 ','添加评论后媒体列表内comments+1','success')
						else:
							self.write_str('1.0.8-2.2 添加评论后媒体列表内comments+1 fail')
							self.write_email_log('1.0.8-2.2 ','添加评论后媒体列表内comments+1','fail')
					else:
						self.write_str("1.0.8-2.1 添加评论 fail")
						self.write_email_log("1.0.8-2.1 ','添加评论","fail")

					#媒体详情比较获取最新的commentId
					mediaInfoResult_end = self.ants_media_detail(mediaId,pid)
					if mediaInfoResult_end != -1 and mediaInfoResult_end !=-100:
						commentList_end = mediaInfoResult_end[0]['commentResList']
						commemtIds = self.get_new_Id(commentList_init,commentList_end)
						
						if commemtIds !=[]:
							commemtId=commemtIds[0]['commentId']
							print(commemtId)
							#删除评论
							delCom = self.ants_del_comment(commemtId,mediaId,persons[1])
							if delCom == 'success':
								self.write_str("1.0.8-2.3 删除评论 success")
								self.write_email_log("1.0.8-2.3 ","删除评论","success")
								vedioIndex_com_end = self.ants_video_index('mediaId',mediaId,'comments',pid)
								print(type(vedioIndex_com),vedioIndex_com)
								print(type(vedioIndex_com_end),vedioIndex_com_end)
								if vedioIndex_com_end ==-1 or vedioIndex_com_end ==-100:
									self.write_str('1.0.8-2.4 删除评论后媒体列表展示异常 error')
									self.write_email_log('1.0.8-2.4 ','删除评论后媒体列表展示异常','error')
								elif vedioIndex_com_end == False:
									self.write_str('1.0.8-2.4 删除评论后媒体列表内comments+1 fail')
									self.write_email_log('1.0.8-2.4 ','删除评论后媒体列表内comments+1','fail')
								elif vedioIndex_com_end[0] ==vedioIndex_com[0]-1:
									self.write_str('1.0.8-2.4 删除评论后媒体列表内comments-1 success')
									self.write_email_log('1.0.8-2.4 ','删除评论后媒体列表内comments-1','success')
								else:
									self.write_str('1.0.8-2.4 删除评论后媒体列表内comments-1 fail')
									self.write_email_log('1.0.8-2.4 ','删除评论后媒体列表内comments-1','fail')
							else:
								self.write_str("1.0.8-2.3 删除评论 fail")
								self.write_email_log("1.0.8-2.3 ","删除评论","fail")

					#===============================关注信息===============================================================================	
					isFollow=mediaInfoResult[0]['isFollow']
					print(isFollow)
					if isFollow ==1:
						#取消关注
						isdelFollow = self.ants_follow(userId,0,pid)
						if isdelFollow == 'success':
							self.write_str('1.0.8-3.1 取消关注 success')
							self.write_email_log('1.0.8-3.1 ','取消关注','success')
							#查看视频列表
							isFollow_videoIndex = self.ants_video_index('mediaId',mediaId,'isFollow',pid)
							print(isFollow)
							if isFollow_videoIndex == [0]:
								self.write_str('1.0.8-3.2 取消关注后媒体列表内isFollow显示正常 success')
								self.write_email_log('1.0.8-3.2 ','取消关注后媒体列表内isFollow显示正常','success')
							else:
								self.write_str('1.0.8-3.2 取消关注后媒体列表内isFollow显示正常 fail')
								self.write_email_log('1.0.8-3.2 ','取消关注后媒体列表内isFollow显示正常','fail')
						else:
							self.write_str('1.0.8-3.1 取消关注失败 fail')
							self.write_email_log('1.0.8-3.1 ','取消关注失败','fail')
					else:
						#添加关注
						isAddFollow= self.ants_follow(userId,1,pid)
						if isAddFollow == 'success':
							self.write_str('1.0.8-3.3 添加关注 success')
							self.write_email_log('1.0.8-3.3 ','添加关注','success')
							isFollow_end = self.ants_video_index('mediaId',mediaId,'isFollow',pid)
							print(isFollow_end)
							if isFollow_end == [1]:
								self.write_str('1.0.8-3.4 添加关注后媒体列表内isFollow显示正常 success')
								self.write_email_log('1.0.8-3.4 ','添加关注后媒体列表内isFollow显示正常','success')
							else:
								self.write_str('1.0.8-3.4 添加关注后媒体列表内isFollow显示正常 fail')
								self.write_email_log('1.0.8-3.4 ','添加关注后媒体列表内isFollow显示正常','fail')
						else:
							self.write_str('1.0.8-3.3 添加关注失败 fail')
							self.write_email_log('1.0.8-3.3 ','添加关注失败','fail')

					#==========================点赞	==================================================	=
					islike = mediaInfoResult[0]['islike']
					bodys = {}
					bodys['mediaId'] = mediaId
					if islike != 1:
						#点赞
						bodys['doLike'] = True
						status=self.ants_like(mediaId,bodys,pid)
						if status == 'success':
							self.write_str('1.0.8-3.1 点赞 success')
							self.write_email_log('1.0.8-3.1 ','点赞','success')  
							#查看视频列表
							vedio_islike = self.ants_video_index('mediaId',mediaId,'islike',pid)
							print(vedio_islike)
							if vedio_islike == [1]:
								self.write_str('1.0.8-3.2 点赞后媒体列表内islike显示正常 success')
								self.write_email_log('1.0.8-3.2 ','点赞后媒体列表内islike显示正常','success')
							else:
								self.write_str('1.0.8-3.2 点赞后媒体列表内islike显示正常 fail')
								self.write_email_log('1.0.8-3.2 ','点赞后媒体列表内islike显示正常','fail')
						else:
							self.write_str('1.0.8-3.1 点赞失败 fail')
							self.write_email_log('1.0.8-3.1 ','点赞失败','fail')      
					else:
						#取消点赞
						bodys['doLike'] = False
						islike_result = self.ants_like(mediaId,bodys,pid)
						if islike_result == 'success':
							self.write_str('1.0.8-3.3 取消点赞 success')
							self.write_email_log('1.0.8-3.3 ','取消点赞','success')
							#查看视频列表
							vedio_mediaId = self.ants_video_index('mediaId',mediaId,'islike',pid)
							print(vedio_mediaId)
							if vedio_mediaId == [0]:
								self.write_str('1.0.8-3.4 取消点赞后媒体列表内islike显示正常 success')
								self.write_email_log('1.0.8-3.4 ','取消点赞后媒体列表内islike显示正常','success')
							else:
								self.write_str('1.0.8-3.4 取消点赞后媒体列表内islike显示正常 fail')
								self.write_email_log('1.0.8-3.4 ','取消点赞后媒体列表内islike显示正常','fail')
						else:
							self.write_str('1.0.8-3.3 取消点赞失败 fail')
							self.write_email_log('1.0.8-3.3 ','取消点赞失败','fail')

					break	


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