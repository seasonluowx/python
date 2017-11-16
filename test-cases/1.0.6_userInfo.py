# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/2/20
import os
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0]
# scriptpath=os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile
import time

class UserInfo(Common):
	def __init__(self, sever,serve_yy,moduleName):
		Common.__init__(self,sever,serve_yy,moduleName)

	def runUserInfo(self,persons):
		isRun =False
		isRunTag = False
		isRunClub = False
		isRunTagPic = False
		isRunClubPic = False
		isDelCom =False
		result = self.get_mediaId()
		mediaId = int(result)
		if mediaId !=0:
			isRun =True

		userId=self.get_pid()
		pid=int(userId)

		if isRun:
			print(mediaId)
			#==============================修改用户姓名=====================================================================
			user_name=self.ants_get_user_info(pid,'name',pid)
			bodys = {}
			if user_name == 'Maple_feng':
				userName='Maple'
			else:
				userName='Maple_feng'
			bodys['name']=userName
			#修改用户姓名信息
			userInfo_time1=self.get_now_time()
			user_putName_result = self.ants_put_user_info(bodys,'name',pid)
			userInfo_time2=self.get_now_time()
			if user_putName_result == userName:
				self.write_str("1.0.6.1 修改用户姓名 success，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
				self.write_email_log("1.0.6.1 ","修改用户姓名，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")

				time.sleep(5)
				#------修改用户姓名影响用户详情 1.1--------
				userInfo_time3=self.get_now_time()
				user_put_name = self.ants_get_user_info(pid,'name',pid)
				userInfo_time4=self.get_now_time()
				if user_put_name == -1 or user_put_name == -100:
					self.write_str("1.0.6.1.1 修改姓名后用户详情异常 error")
					self.write_email_log('1.0.6.1.1 ','修改姓名后用户详情异常','error')
				elif user_put_name == userName:
					self.write_str("1.0.6.1.1 修改姓名影响用户个人信息列表 success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
					self.write_email_log("1.0.6.1.1 ","修改姓名影响用户个人信息列表，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
				else:
					self.write_str("1.0.6.1.1 修改姓名影响用户个人信息列表 fail")
					self.write_email_log("1.0.6.1.1 ","修改姓名影响用户个人信息列表","fail")

				#------修改用户姓名影响首页列表 1.2---------
				find_time1 =self.get_now_time()
				user_find_name = self.ants_index('mediaId',mediaId,'userName',pid)
				find_time2=self.get_now_time()
				if user_find_name == -1 or user_find_name == -100:
					self.write_str("1.0.6.1.2 修改姓名后首页列表异常 error")
					self.write_email_log('1.0.6.1.2 ','修改姓名后首页列表异常','error')
				elif user_find_name == False:
					self.write_str("1.0.6.1.2 修改姓名影响首页列表 fail")
					self.write_email_log('1.0.6.1.2 ','修改姓名影响首页列表','fail')
				elif user_find_name[0] == userName:
					self.write_str('1.0.6.1.2 修改姓名影响首页列表 success，耗时'+str(self.get_time_long(find_time1,find_time2)))
					self.write_email_log("1.0.6.1.2 ","修改姓名影响首页列表，耗时"+str(self.get_time_long(find_time1,find_time2)),"success")
				else:
					self.write_str("1.0.6.1.2 修改姓名影响首页列表 fail")
					self.write_email_log('1.0.6.1.2 ','修改姓名影响首页列表','fail')

				#---------修改用户姓名影响媒体详情--------
				detail_time1 =self.get_now_time()
				user_detail_name = self.ants_media_detail(mediaId,pid)
				detail_time2=self.get_now_time()
				if user_detail_name == -1 or user_detail_name == -100:
					self.write_str("1.0.6.1.3 修改姓名后媒体详情异常 error")
					self.write_email_log('1.0.6.1.3 ','修改姓名后媒体详情异常','error')
				elif user_detail_name[0]['userName'] == userName:
					self.write_str('1.0.6.1.3 修改姓名影响媒体详情 success，耗时'+str(self.get_time_long(detail_time1,detail_time2)))
					self.write_email_log("1.0.6.1.3 ","修改姓名影响媒体详情","success")
					
					#获取tag信息
					tags = user_detail_name[0]['tags']
					if tags != '':
						tagIds=tags.split(",")
						tagId=tagIds[0]
						isRunTag = True
						print('tagId:'+str(tagId))
         			 #获取club信息   
					tagList_init = user_detail_name[0]['tagList']
					for x in range(len(tagList_init)):
						if tagList_init[x]['mediaSpecial'] == 10:
							clubId=tagList_init[x]['id']
							isRunClub =True
							print('clubId:'+str(clubId))
				else:
					self.write_str('1.0.6.1.3 修改姓名影响媒体详情 fail')
					self.write_email_log("1.0.6.1.3 ","修改姓名影响媒体详情","fail")


				#-------修改用户姓名影响标签最新列表 1.4----
				if isRunTag:
					city_time1=self.get_now_time()
					tag_least_userName = self.ants_tags_least(tagId,'mediaId',mediaId,'userName',persons[1])
					print(tag_least_userName)
					city_time2=self.get_now_time()
					if tag_least_userName == -1 or tag_least_userName == -100:
						self.write_str('1.0.6.1.4 修改姓名影响标签最新列表 fail')
						self.write_email_log("1.0.6.1.4 ","修改姓名影响标签最新列表","fail")
					elif tag_least_userName[0] == userName:
						self.write_str('1.0.6.1.4 修改姓名影响标签最新列表 success，耗时'+str(self.get_time_long(city_time1,city_time2)))
						self.write_email_log("1.0.6.1.4 ","修改姓名影响标签最新列表，耗时"+str(self.get_time_long(city_time1,city_time2)),"success")
					else:
						self.write_str('1.0.6.1.4 修改姓名影响标签最新列表 fail')
						self.write_email_log("1.0.6.1.4 ","修改姓名影响标签最新列表","fail")

				# ---------修改用户姓名影响评价信息--------
				#添加评论
				bodys_cn = {}
				bodys_cn['content'] = self.get_random() + ' === Good !===> '+ self.get_local_time()
				bodys_cn['mediaId'] = mediaId
				bodys_cn['userId'] = persons[1]
				add_comment_result = self.ants_add_comment(mediaId,bodys_cn,pid)
				if add_comment_result == 'success':
					time.sleep(5)

					detail_time3=self.get_now_time()
					#查看媒体详情
					media_comName=self.ants_media_detail(mediaId,pid)
					if media_comName == -1 or media_comName == -100:
						self.write_str("1.0.6.1.5 修改姓名并添加评论后媒体详情异常 error")
						self.write_email_log('1.0.6.1.5 ","修改姓名并添加评论后媒体详情异常','error')
					else:
						detail_time4=self.get_now_time()
						media_comNameList = media_comName[0]['commentResList']
						commentId = media_comNameList[0]['commentId']
						isDelCom = True
						if media_comNameList[0]['authorName'] == userName:
							self.write_str('1.0.6.1.5 修改姓名影响媒体详情内评价信息 success，耗时'+str(self.get_time_long(detail_time3,detail_time4)))
							self.write_email_log("1.0.6.1.5 ","修改姓名影响媒体详情内评价信息，耗时"+str(self.get_time_long(detail_time3,detail_time4)),"success")
						else:
							self.write_str('1.0.6.1.5 修改姓名影响媒体详情内评价信息 fail')
							self.write_email_log("1.0.6.1.5 ","修改姓名影响媒体详情内评价信息","fail")
												 
					#查看评论列表
					cnList_time1=self.get_now_time()
					media_comList_name = self.ants_get_comments_list(mediaId,pid)
					cnList_time2=self.get_now_time()
					if media_comList_name==-1 or media_comList_name== -100:
						self.write_str("1.0.6.1.6 修改姓名并添加评论后评论列表异常 error")
						self.write_email_log('1.0.6.1.6 ","修改姓名并添加评论后评论列表异常','error')
					elif media_comList_name[0]['authorName'] == userName:
						self.write_str('1.0.6.1.6 修改姓名影响评价列表 success，耗时'+str(self.get_time_long(cnList_time1,cnList_time2)))
						self.write_email_log("1.0.6.1.6 ","修改姓名影响评价列表，耗时"+str(self.get_time_long(cnList_time1,cnList_time2)),"success")
					else:
						self.write_str('1.0.6.1.6 修改姓名影响评价列表 fail')
						self.write_email_log("1.0.6.1.6 ","修改姓名影响评价列表","fail")

					time.sleep(10)
					#消息列表mediaId,1,2,persons[1],ax,pid)
					msg_time1=self.get_now_time()
					ax ={'commentContent': bodys_cn['content']}
					comMsgList = self.ants_get_msg(mediaId,1,3,pid,ax,persons[1])
					print(comMsgList)
					msg_time2=self.get_now_time()
					if comMsgList==-1 or comMsgList == -100:
						self.write_str("1.0.6.1.7 修改姓名并添加评论后消息列表异常 error")
						self.write_email_log('1.0.6.1.7 ","修改姓名并添加评论后消息列表异常','error')
					elif comMsgList == False:
						self.write_str('1.0.6.1.7 修改姓名影响评论消息 fail')
						self.write_email_log('1.0.6.1.7 ","修改姓名影响评论消息','fail')
					elif comMsgList['name'] == userName:
						self.write_str('1.0.6.1.7 修改姓名影响评论消息 success，耗时'+str(self.get_time_long(msg_time1,msg_time2)))
						self.write_email_log("1.0.6.1.7 ","修改姓名影响评论消息，耗时"+str(self.get_time_long(msg_time1,msg_time1)),'success')
					else:
						self.write_str('1.0.6.1.7 修改姓名影响评论消息 fail')
						self.write_email_log('1.0.6.1.7 ","修改姓名影响评论消息','fail')

					#删除评论
					if isDelCom:
						self.ants_del_comment(commentId,mediaId,pid)

				#--------修改用户姓名影响俱乐部话题列表----
				if isRunClub:
					indexFollow_time1=self.get_now_time()
					club_userName = self.ants_club_latest(clubId,'mediaId',mediaId,'userName',pid)
					print(club_userName)
					indexFollow_time2=self.get_now_time()
					if club_userName== -1 or club_userName == -100:
						self.write_str("1.0.6.1.8 修改用户姓名后俱乐部话题列表异常 error")
						self.write_email_log("1.0.6.1.8 ","修改用户姓名后俱乐部话题列表异常","error")
					elif club_userName[0] == userName:
						self.write_str('1.0.6.1.8 修改用户姓名影响俱乐部话题列表 success，耗时'+str(self.get_time_long(indexFollow_time1,indexFollow_time2)))
						self.write_email_log("1.0.6.1.8 ","修改用户姓名影响俱乐部话题列表，耗时"+str(self.get_time_long(indexFollow_time1,indexFollow_time2)),"success")
					else:
						self.write_str("1.0.6.1.8 修改用户姓名影响俱乐部话题列表 fail")
						self.write_email_log("1.0.6.1.8 ","修改用户姓名影响俱乐部话题列表","fail")

				#--------------------修改姓名影响关注列表---------------------------------
				follow_result = self.ants_fllowList(pid,1,persons[1])
				if follow_result == False:
					#添加关注
					add_follow_result=self.ants_follow(pid,1,persons[1])
					if add_follow_result == 'success':
						self.write_str('添加关注 success')

				#查看follow列表
				followList_time1=self.get_now_time()
				user_follow_name = self.ants_fllowList(pid,1,persons[1])
				followList_time2=self.get_now_time()
				print(user_follow_name)
				if user_follow_name == -1 or user_follow_name == -100:
					self.write_str('1.0.6.1.9 修改用户姓名后关注列表异常 error')
					self.write_email_log('1.0.6.1.9 ','修改用户姓名后关注列表异常 ','error')
				elif user_follow_name == False:
					self.write_str('1.0.6.1.9 修改用户姓名影响关注列表 fail')
					self.write_email_log('1.0.6.1.9 ','修改用户姓名影响关注列表 ','fail')
				elif user_follow_name['name'] == userName:
					self.write_str('1.0.6.1.9 修改用户姓名影响关注列表 success，耗时'+str(self.get_time_long(followList_time1,followList_time2)))
					self.write_email_log('1.0.6.1.9 ','修改用户姓名影响关注列表 ，耗时'+str(self.get_time_long(followList_time1,followList_time2)),'success')
				else:
					self.write_str('1.0.6.1.9 修改用户姓名影响关注列表 fail')
					self.write_email_log('1.0.6.1.9 ','修改用户姓名影响关注列表 ','fail')

				#取消关注
				self.ants_follow(pid,0,persons[1])

				# #--------------------修改姓名影响粉丝列表---------------------------------
				fans_result = self.ants_fansList(persons[1],-1,pid)
				print(fans_result)
				if fans_result == False:
					#添加关注
					add_fan_result=self.ants_follow(persons[1],1,pid)
					if add_fan_result == 'success':
						self.write_str("添加关注成功")

						time.sleep(5)

						#查看消息列表0,2,4,persons[1],ax,pid
						msg_time3=self.get_now_time()
						comMsgList = self.ants_get_msg(0,2,4,pid,{},persons[1])
						msg_time4=self.get_now_time()
						print(comMsgList)
						if comMsgList == -1 or comMsgList == -100:
							self.write_str('1.0.6.1.10 修改姓名后，被关注用户消息列表异常 fail')
							self.write_email_log('1.0.6.1.10 ','修改姓名后，被关注用户消息列表异常','fail')
						elif comMsgList == False:
							self.write_str('1.0.6.1.10 修改姓名影响关注消息 fail')
							self.write_email_log('1.0.6.1.10 ','修改姓名影响关注消息','fail')
						elif comMsgList['name'] == userName:
							self.write_str('1.0.6.1.10 修改姓名影响关注消息 success，耗时'+str(self.get_time_long(msg_time3,msg_time4)))
							self.write_email_log("1.0.6.1.10 ","修改姓名影响关注消息，耗时"+str(self.get_time_long(msg_time3,msg_time4)),'success')
						else:
							self.write_str('1.0.6.1.10 修改姓名影响关注消息 fail')
							self.write_email_log('1.0.6.1.10 ','修改姓名影响关注消息','fail')

				#查看粉丝列表内容
				fanList_time1=self.get_now_time()
				user_fans_name=self.ants_fansList(persons[1],-1,pid)
				fanList_time2=self.get_now_time()
				print(user_fans_name)
				if user_fans_name == -1 or user_fans_name == -100:
					self.write_str('1.0.6.1.11 修改用户姓名后查看粉丝列表异常 error')
					self.write_email_log('1.0.6.1.11 ','修改用户姓名后查看粉丝列表异常 ','error')
				elif user_fans_name == False:
					self.write_str('1.0.6.1.11 修改用户姓名影响粉丝列表 fail')
					self.write_email_log('1.0.6.1.11 ','修改用户姓名影响粉丝列表 ','fail')
				elif user_fans_name['name'] == userName:
					self.write_str('1.0.6.1.11 修改用户姓名影响粉丝列表 success，耗时'+str(self.get_time_long(fanList_time1,fanList_time2)))
					self.write_email_log('1.0.6.1.11 ','修改用户姓名影响粉丝列表，耗时'+str(self.get_time_long(fanList_time1,fanList_time2)),'success')
				else:
					self.write_str('1.0.6.1.11 修改用户姓名影响粉丝列表 fail')
					self.write_email_log('1.0.6.1.11 ','修改用户姓名影响粉丝列表 ','fail')
				#取消关注
				self.ants_follow(persons[1],0,pid)

				#修改姓名影响用户搜索界面
				fanList_time1=self.get_now_time()
				user_fans_name=self.ants_searchUser(userName,pid,pid)
				fanList_time2=self.get_now_time()
				print(user_fans_name)
				if user_fans_name == -1 or user_fans_name == -100:
					self.write_str('1.0.6.1.12 修改用户姓名用户搜索界面异常 error')
					self.write_email_log('1.0.6.1.12 ','修改用户姓名用户搜索界面异常 ','error')
				elif user_fans_name== False:
					self.write_str('1.0.6.1.12 修改用户姓名影响用户搜索界面 fail')
					self.write_email_log('1.0.6.1.12 ','修改用户姓名影响用户搜索界面 ','fail')
				elif user_fans_name['isFollow'] == -1:
					self.write_str('1.0.6.1.12 修改用户姓名影响用户搜索界面 success')
					self.write_email_log('1.0.6.1.12 ','修改用户姓名影响用户搜索界面 ','success')
				else:
					self.write_str('1.0.6.1.12 修改用户姓名影响用户搜索界面 fail')
					self.write_email_log('1.0.6.1.12 ','修改用户姓名影响用户搜索界面 ','fail')

				#修改姓名影响标签用户列表
				if isRunTag:
					city_time1=self.get_now_time()
					tag_user = self.ants_tagUser(tagId,pid,pid)
					print(tag_user)
					city_time2=self.get_now_time()
					if tag_user == -1 or tag_user == -100:
						self.write_str('1.0.6.1.13 修改姓名影响标签用户列表 error')
						self.write_email_log("1.0.6.1.13 ","修改姓名影响标签用户列表","error")
					elif tag_user == False:
						self.write_str('1.0.6.1.13 修改姓名影响标签用户列表 fail')
						self.write_email_log("1.0.6.1.13 ","修改姓名影响标签用户列表","fail")
					elif tag_user['name'] == userName:
						self.write_str('1.0.6.1.13 修改姓名影响标签用户列表 success，耗时'+str(self.get_time_long(city_time1,city_time2)))
						self.write_email_log("1.0.6.1.13 ","修改姓名标签用户列表，耗时"+str(self.get_time_long(city_time1,city_time2)),"success")
					else:
						self.write_str('1.0.6.1.13 修改姓名影响标签用户列表 fail')
						self.write_email_log("1.0.6.1.13 ","修改姓名影响标签用户列表","fail")
			else:
				self.write_str("1.0.6.1 修改用户姓名 fail")
				self.write_email_log("1.0.6.1 ","修改用户姓名","fail")
	   #=====================================================================================================================    

	   #=======================修改头像=============================
	    	#查看用户详情
			userInitIcon = self.ants_get_user_info(pid,'icon',pid)
			print(userInitIcon)
			userInfo_time5=self.get_now_time()
	    	#获取媒体上传url
			media = 'mao.jpg'
			urlId,url,urlType = self.ants_get_icon_fileId(media,pid)

			
		    #上传mediaUrl,media,thumbUrl,thumb
			for x in range(1,10):
				isUpLoadResult = self.ants_upload_local_video_work(url,media,'','')
				print(isUpLoadResult)
				if isUpLoadResult == True:
					self.write_str('1.0.6 头像第'+str(x)+'次上传成功')
					self.write_email_log('1.0.6','头像第'+str(x)+'次上传成功','success')

					bodys = {}
					bodys['iconUrlId']=urlId
					bodys['urlType']=urlType
					print(urlId)
		    		#修改用户头像
					user_putPic_result = self.ants_put_user_info(bodys,'message',pid)
					userInfo_time6=self.get_now_time()
					print(user_putPic_result)
					if user_putPic_result == 'success':
						self.write_str('1.0.6.2 用户修改头像 success，耗时'+str(self.get_time_long(userInfo_time5,userInfo_time6)))
						self.write_email_log("1.0.6.2 ","用户修改头像"+str(self.get_time_long(userInfo_time5,userInfo_time6)),"success")

						time.sleep(5)

						#-------------修改头像影响用户详情---------------------
						detail_time5=self.get_now_time()
						userNewIcon = self.ants_get_user_info(pid,'icon',pid)
						detail_time6=self.get_now_time()
						print(userNewIcon)
						print(userInitIcon)
						if userNewIcon == -1 or userNewIcon== -100:
							self.write_str('1.0.6.2.1 修改头像后访问用户详情异常 error')
							self.write_email_log('1.0.6.2.1 ','修改头像后访问用户详情异常','error')
						elif userInitIcon == userNewIcon:
							self.write_str('1.0.6.2.1 修改头像影响用户详情 fail')
							self.write_email_log('1.0.6.2.1 ','修改头像影响用户详情','fail')
						else:
							self.write_str('1.0.6.2.1 修改头像影响用户详情 success，耗时'+str(self.get_time_long(detail_time5,detail_time6)))
							self.write_email_log('1.0.6.2.1 ','修改头像影响用户详情，耗时'+str(self.get_time_long(detail_time5,detail_time6)),'success')

						#-------------修改头像影响首页列表--------------------
						find_time3=self.get_now_time()
						user_find_pic = self.ants_index('mediaId',mediaId,'userIcon',pid)
						find_time4=self.get_now_time()
						print(user_find_pic)
						if user_find_pic == -1 or user_find_pic == -100:
							self.write_str("1.0.6.2.2 修改头像后首页列表异常 error")
							self.write_email_log('1.0.6.2.2 ','修改头像后首页列表异常','error')
						elif user_find_pic[0] == userNewIcon:
							self.write_str('1.0.6.2.2 修改头像影响首页列表 success，耗时'+str(self.get_time_long(find_time3,find_time4)))
							self.write_email_log('1.0.6.2.2 ','修改头像影响首页列表，耗时'+str(self.get_time_long(find_time3,find_time4)),'success')
						else:
							self.write_str('1.0.6.2.2 修改头像影响首页列表 fail')
							self.write_email_log('1.0.6.2.2 ','修改头像影响首页列表','fail')

						#------------修改头像影响媒体详情--------
						detail_time7=self.get_now_time()
						user_detai_pic = self.ants_media_detail(mediaId,pid)
						detail_time8=self.get_now_time()
						print(user_detai_pic)
						if user_detai_pic == -1 or user_detai_pic== -100:
							self.write_str('1.0.6.2.3 修改头像后访问媒体详情异常 error')
							self.write_email_log('1.0.6.2.3 ','修改头像后访问媒体详情异常','error')
						elif user_detai_pic[0]['userIcon'] == userNewIcon:
							self.write_str('1.0.6.2.3 修改头像影响媒体详情 success，耗时'+str(self.get_time_long(detail_time7,detail_time8)))
							self.write_email_log('1.0.6.2.3 ','修改头像影响媒体详情，耗时'+str(self.get_time_long(detail_time7,detail_time8)),'success')

							#获取tag信息
							tags = user_detai_pic[0]['tags']
							if tags != '':
								tagIds=tags.split(",")
								tagId=tagIds[0]
								isRunTagPic = True
								print('tagId:'+str(tagId))

		          			#获取club信息   
							tagList_init = user_detai_pic[0]['tagList']
							for x in range(len(tagList_init)):
								if tagList_init[x]['mediaSpecial'] == 10:
									clubId=tagList_init[x]['id']
									isRunClubPic =True
									print('clubId:'+str(clubId))
						else:
							self.write_str('1.0.6.2.3 修改头像影响媒体详情 fail')
							self.write_email_log('1.0.6.2.3 ','修改头像影响媒体详情','fail')


						#-------修改用户头像影响标签最新列表 1.4----
						if isRunTagPic:
							city_time1=self.get_now_time()
							tag_least_userIcon = self.ants_tags_least(tagId,'mediaId',mediaId,'userIcon',persons[1])
							print(tag_least_userIcon)
							city_time2=self.get_now_time()
							if tag_least_userIcon == -1 or tag_least_userIcon == -100:
								self.write_str('1.0.6.2.4 修改头像影响标签最新列表 fail')
								self.write_email_log("1.0.6.2.4 ","修改头像影响标签最新列表","fail")
							elif tag_least_userIcon[0] == userNewIcon:
								self.write_str('1.0.6.2.4 修改头像影响标签最新列表 success，耗时'+str(self.get_time_long(city_time1,city_time2)))
								self.write_email_log("1.0.6.2.4 ","修改头像影响标签最新列表，耗时"+str(self.get_time_long(city_time1,city_time2)),"success")
							else:
								self.write_str('1.0.6.2.4 修改头像影响标签最新列表 fail')
								self.write_email_log("1.0.6.2.4 ","修改头像影响标签最新列表","fail")

				

						#---------------修改头像影响评论信息-------
						#添加评论
						bodys_cn = {}
						bodys_cn['content'] = self.get_random() + ' === Good !===> '+ self.get_local_time()
						bodys_cn['mediaId'] = mediaId
						bodys_cn['userId'] = persons[1]
						add_comment_result = self.ants_add_comment(mediaId,bodys_cn,pid)
						if add_comment_result == 'success':
							#-------修改头像影响媒体详情内的评论信息---------
							time.sleep(5)
							
							detail_time9=self.get_now_time()
							user_com_pic = self.ants_media_detail(mediaId,pid)
							if user_com_pic == -1 or user_com_pic == -100:
								self.write_str("1.0.6.2.5 修改头像并添加评论后媒体详情异常 error")
								self.write_email_log('1.0.6.2.5 ','修改头像并添加评论后媒体详情异常','error')
							else:
								media_comPicList = user_com_pic[0]['commentResList']
								commentId = media_comPicList[0]['commentId']
								detail_time10=self.get_now_time()
								if media_comPicList[0]['authorIcon'] == userNewIcon:
									self.write_str('1.0.6.2.5 修改头像影响媒体详情内评论信息 success，耗时'+str(self.get_time_long(detail_time9,detail_time10)))
									self.write_email_log('1.0.6.2.5 ','修改头像影响媒体详情内评论信息，耗时'+str(self.get_time_long(detail_time9,detail_time10)),'success')
								else:
									self.write_str('1.0.6.2.5 修改头像影响媒体详情内评论信息 fail')
									self.write_email_log('1.0.6.2.5 ','修改头像影响媒体详情内评论信息 ','fail')

							#------------修改头像影响评论列表----------
							cnList_time3=self.get_now_time()
							user_comList_pic = self.ants_get_comments_list(mediaId,pid)
							cnList_time4=self.get_now_time()
							if user_comList_pic==-1 or user_comList_pic== -100:
								self.write_str("1.0.6.2.6 修改头像并添加评论后评论列表异常 error")
								self.write_email_log('1.0.6.2.6 ','修改头像并添加评论后评论列表异常','error')
							elif user_comList_pic[0]['authorIcon'] == userNewIcon:
								self.write_str('1.0.6.2.6 修改头像影响评论列表 success，耗时'+str(self.get_time_long(cnList_time3,cnList_time4)))
								self.write_email_log('1.0.6.2.6 ','修改头像影响评论列表，耗时'+str(self.get_time_long(cnList_time3,cnList_time4)),'success')
							else:
								self.write_str('1.0.6.2.6 修改头像影响评论列表 fail')
								self.write_email_log('1.0.6.2.6 ','修改头像影响评论列表','fail')

							time.sleep(10)
							#-------------修改头像影响消息列表---------
							msg_time5=self.get_now_time()
							ax ={'commentContent': bodys_cn['content']}
							comMsgList_icon_ants = self.ants_get_msg(mediaId,1,3,pid,ax,persons[1])
							msg_time6=self.get_now_time()
							print(comMsgList_icon_ants)
							print('==============================')
							if comMsgList_icon_ants==-1 or comMsgList_icon_ants == -100:
								self.write_str("1.0.6.2.7 修改头像并添加评论后消息列表异常 error")
								self.write_email_log('1.0.6.2.7 ','修改头像并添加评论后消息列表异常','error')
							elif comMsgList_icon_ants == False:
								self.write_str('1.0.6.2.7 修改头像影响评论消息 fail')
								self.write_email_log('1.0.6.2.7 ','修改头像影响评论消息','fail')
							elif comMsgList_icon_ants['icon']==userNewIcon:
								self.write_str('1.0.6.2.7 修改头像影响评论消息列表 success，耗时'+str(self.get_time_long(msg_time5,msg_time6)))
								self.write_email_log('1.0.6.2.7 ','修改头像影响评论消息列表，耗时'+str(self.get_time_long(msg_time5,msg_time6)),'success')
							else:
								self.write_str('1.0.6.2.7 修改头像影响评论消息列表 fail')
								self.write_email_log('1.0.6.2.7 ','修改头像影响评论消息列表','fail')


							#删除评论
							self.ants_del_comment(commentId,mediaId,pid)

							#--------修改用户头像影响俱乐部话题列表----
							if isRunClubPic:
								indexFollow_time1=self.get_now_time()
								club_userIcon = self.ants_club_latest(clubId,'mediaId',mediaId,'userIcon',pid)
								print(club_userIcon)
								indexFollow_time2=self.get_now_time()
								if club_userIcon== -1 or club_userIcon == -100:
									self.write_str("1.0.6.2.8 修改用户头像后俱乐部话题列表异常 error")
									self.write_email_log("1.0.6.2.8 ","修改用户头像后俱乐部话题列表异常","error")
								elif club_userIcon[0] == userNewIcon:
									self.write_str('1.0.6.2.8 修改用户头像影响俱乐部话题列表 success，耗时'+str(self.get_time_long(indexFollow_time1,indexFollow_time2)))
									self.write_email_log("1.0.6.2.8 ","修改用户头像影响俱乐部话题列表，耗时"+str(self.get_time_long(indexFollow_time1,indexFollow_time2)),"success")
								else:
									self.write_str("1.0.6.2.8 修改用户头像影响俱乐部话题列表 fail")
									self.write_email_log("1.0.6.2.8 ","修改用户头像影响俱乐部话题列表","fail")

							#--------------------修改头像影响关注列表---------------------------------
							follow_result = self.ants_fllowList(pid,1,persons[1])
							if follow_result == False:
								#添加关注
								add_follow_result=self.ants_follow(pid,1,persons[1])
								if add_follow_result == 'success':
									self.write_str('添加关注 success')

							followList_time3=self.get_now_time()		
							#查看follow列表
							user_follow_icon = self.ants_fllowList(pid,1,persons[1])
							followList_time4=self.get_now_time()
							if user_follow_icon == -1 or user_follow_icon == -100:
								self.write_str('1.0.6.2.9 修改用户头像后关注列表异常 error')
								self.write_email_log('1.0.6.1.9 ','修改用户头像后关注列表异常 ','error')
							elif user_follow_icon == False:
								self.write_str('1.0.6.1.9 修改用户头像影响关注列表 fail')
								self.write_email_log('1.0.6.1.9 ','修改用户头像影响关注列表 ','fail')
							elif user_follow_icon['icon'] == userNewIcon:
								self.write_str('1.0.6.2.9 修改头像影响关注列表 success，耗时'+str(self.get_time_long(followList_time3,followList_time4)))
								self.write_email_log('1.0.6.2.9 ','修改头像影响关注列表，耗时'+str(self.get_time_long(followList_time3,followList_time4)),'success')
							else:
								self.write_str('1.0.6.2.9 修改头像影响关注列表 fail')
								self.write_email_log('1.0.6.2.9 ','修改头像影响关注列表 ','fail')

							#取消关注
							self.ants_follow(pid,0,persons[1])


						# #--------------------修改头像影响粉丝列表和关注消息---------------------------------
						fans_result = self.ants_fansList(persons[1],-1,pid)
						if fans_result == False:
							#添加关注
							add_fan_result=self.ants_follow(persons[1],1,pid)
							if add_fan_result == 'success':
								self.write_str("添加关注成功")
								msg_time7=self.get_now_time()

								time.sleep(5)
								#查看消息列表
								msg_time7=self.get_now_time()
								ax_follow={}
								comMsgList_icon = self.ants_get_msg(0,2,4,pid,ax_follow,persons[1])
								msg_time8=self.get_now_time()
								print(comMsgList_icon)
								if comMsgList_icon == -1 or comMsgList_icon == -100:
									self.write_str('1.0.6.2.10 修改头像后，被关注用户消息列表异常 fail')
									self.write_email_log('1.0.6.2.10 ','修改头像后，被关注用户消息列表异常','fail')
								elif comMsgList_icon == False:
									self.write_str('1.0.6.2.10 修改头像影响关注消息 fail')
									self.write_email_log('1.0.6.2.10 ','修改头像影响关注消息','fail')
								elif comMsgList_icon['icon'] == userNewIcon:
									self.write_str('1.0.6.2.10 修改头像影响关注消息 success，耗时'+str(self.get_time_long(msg_time7,msg_time8)))
									self.write_email_log("1.0.6.2.10","修改头像影响关注消息，耗时"+str(self.get_time_long(msg_time7,msg_time8)),'success')
								else:
									self.write_str('1.0.6.2.10 修改头像影响关注消息 fail')
									self.write_email_log('1.0.6.2.10 ','修改头像影响关注消息','fail')
			

						#查看粉丝列表内容
						fanList_time3=self.get_now_time()
						user_fans_name=self.ants_fansList(persons[1],-1,pid)
						fanList_time4=self.get_now_time()
						print(user_fans_name)
						if user_fans_name == -1 or user_fans_name == -100:
							self.write_str('1.0.6.2.11 修改用户头像后查看粉丝列表异常 error')
							self.write_email_log('1.0.6.2.11 ','修改用户头像后查看粉丝列表异常 ','error')
						elif user_fans_name == False:
							self.write_str('1.0.6.2.11 修改用户头像影响粉丝列表 fail')
							self.write_email_log('1.0.6.2.11 ','修改用户头像影响粉丝列表 ','fail')
						elif user_fans_name['icon'] == userNewIcon:
							self.write_str('1.0.6.2.11 修改头像影响粉丝列表 success，耗时'+str(self.get_time_long(fanList_time3,fanList_time4)))
							self.write_email_log('1.0.6.2.11 ','修改头像影响粉丝列表，耗时'+str(self.get_time_long(fanList_time3,fanList_time4)),'success')
						else:
							self.write_str('1.0.6.2.11 修改头像影响粉丝列表 fail')
							self.write_email_log('1.0.6.2.11 ','修改头像头像影响粉丝列表 ','fail')
						#取消关注
						self.ants_follow(persons[1],0,pid)

						#修改头像影响用户搜索界面
						fanList_time1=self.get_now_time()
						user_fans_name=self.ants_searchUser(userName,pid,pid)
						fanList_time2=self.get_now_time()
						print(user_fans_name)
						if user_fans_name == -1 or user_fans_name == -100:
							self.write_str('1.0.6.2.12 修改用户头像用户搜索界面异常 error')
							self.write_email_log('1.0.6.2.12 ','修改用户头像用户搜索界面异常 ','error')
						elif user_fans_name== False:
							self.write_str('1.0.6.2.12 修改用户头像影响用户搜索界面 fail')
							self.write_email_log('1.0.6.2.11 ','修改用户头像影响用户搜索界面 ','fail')
						elif user_fans_name['icon'] == userNewIcon:
							self.write_str('1.0.6.2.12 修改用户头像影响用户搜索界面 success')
							self.write_email_log('1.0.6.2.12 ','修改用户头像影响用户搜索界面 ','success')
						else:
							self.write_str('1.0.6.2.12 修改用户头像影响用户搜索界面 fail')
							self.write_email_log('1.0.6.2.11 ','修改用户头像影响用户搜索界面 ','fail')

						#修改头像影响标签用户列表
						if isRunTag:
							city_time1=self.get_now_time()
							tag_user = self.ants_tagUser(tagId,pid,pid)
							print(tag_user)
							city_time2=self.get_now_time()
							if tag_user == -1 or tag_user == -100:
								self.write_str('1.0.6.2.13 修改头像影响标签用户列表 error')
								self.write_email_log("1.0.6.2.13 ","修改头像影响标签用户列表","error")
							elif tag_user == False:
								self.write_str('1.0.6.2.13 修改头像影响标签用户列表 fail')
								self.write_email_log("1.0.6.2.13 ","修改头像影响标签用户列表","fail")
							elif tag_user['icon'] == userNewIcon:
								self.write_str('1.0.6.2.13 修改头像影响标签用户列表 success，耗时'+str(self.get_time_long(city_time1,city_time2)))
								self.write_email_log("1.0.6.2.13 ","修改头像标签用户列表，耗时"+str(self.get_time_long(city_time1,city_time2)),"success")
							else:
								self.write_str('1.0.6.2.13 修改头像影响标签用户列表 fail')
								self.write_email_log("1.0.6.2.13 ","修改头像影响标签用户列表","fail")

					else:
						self.write_str('1.0.6.2 用户修改头像 fail')
						self.write_email_log('1.0.6.2 ','用户修改头像','fail')
					break
				else:
					self.write_str('1.0.6 头像第'+str(x)+'次上传失败')
					self.write_email_log('1.0.6','头像第'+str(x)+'次上传失败','fail')
					continue

		#===================================================================================================================== 
			#系统推荐用户
			for i in range(1,4):
				recomUser_time1=self.get_now_time()
				recom_user = self.ants_recomUser(pid)
				recomUser_time2=self.get_now_time()
				print(recom_user)
				if recom_user == -1 or recom_user == -100:
					self.write_str('1.0.6.3 系统推荐用户接口第'+str(i)+'次异常 error')
					self.write_email_log('1.0.6.3 ','系统推荐用户接口第'+str(i)+'次异常','error')
				elif len(recom_user)>0:
					msg = 1
					for x in range(len(recom_user)-1):
						if pid == (recom_user[x]['userId']):
							self.write_str('1.0.6.3 系统推荐用户第'+str(i)+'次返回登录用户信息了 fail')
							self.write_email_log('1.0.6.3 ','系统推荐用户第'+str(i)+'次接口返回登录用户信息了','fail')
							msg = -1
							
							#判断用户姓名修改是否成功修改推荐用户
							if recom_user[x]['name'] ==userName:
								self.write_str('1.0.6.1.15 修改姓名影响推荐用户列表  success')
								self.write_email_log('1.0.6.1.15 ','修改姓名影响推荐用户','success')
							else:
								self.write_str('1.0.6.1.15 修改姓名影响推荐用户 fail')
								self.write_email_log('1.0.6.1.15 ','修改姓名影响推荐用户','fail')

							#判断用户头像修改是否成功修改推荐用户
							print(recom_user[x]['icon'])
							print(userNewIcon)
							if recom_user[x]['icon'] ==userNewIcon:
								self.write_str('1.0.6.2.15 修改头像影响推荐用户列表  success')
								self.write_email_log('1.0.6.2.15 ','修改头像影响推荐用户列表','success')
							else:
								self.write_str('1.0.6.2.15 修改头像影响推荐用户列表 fail')
								self.write_email_log('1.0.6.2.15 ','修改头像影响推荐用户列表','fail')
							break

						elif recom_user[x]['status'] != 0:
							self.write_str('1.0.6.3 系统推荐用户第'+str(i)+'次返回已关注用户信息了 fail')
							self.write_email_log('1.0.6.3 ','系统推荐用户接口第'+str(i)+'次返回已关注用户信息了','fail')
							msg = -1
							break
					if msg ==1:
						self.write_str('1.0.6.3 系统推荐用户第'+str(i)+'次返回数据正常 success,耗时：'+str(self.get_time_long(recomUser_time1,recomUser_time2)))
						self.write_email_log('1.0.6.3 ','系统推荐用户第'+str(i)+'次返回数据正常,耗时：'+str(self.get_time_long(recomUser_time1,recomUser_time2)),'success')	
				else:
					self.write_str('1.0.6.3 系统推荐用户接口第'+str(i)+'次返回数据为空 fail')
					self.write_email_log('1.0.6.3 ','系统推荐用户接口第'+str(i)+'次返回数据为空','fail')

			#热门用户
			carouselsUser_time1=self.get_now_time()
			carousels_user = self.ants_carousels('users',pid)
			carouselsUser_time2=self.get_now_time()
			print(carousels_user)
			if carousels_user==-1 or carousels_user == -100:
				self.write_str('1.0.6.4 热门用户接口异常 error')
				self.write_email_log('1.0.6.4 ','热门用户接口异常','error')
			elif len(carousels_user)>0:
				self.write_str('1.0.6.4 热门用户接口访问正常 success,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)))
				self.write_email_log('1.0.6.4 ','热门用户接口正常,耗时：'+str(self.get_time_long(carouselsUser_time1,carouselsUser_time2)),'success')
				for x in range(len(carousels_user)-1):
					#如果热门用户存在登录用户
					if carousels_user[x]['userId'] == pid:
						#判断用户姓名修改是否成功修改热门用户
						if carousels_user[x]['name'] ==userName:
							self.write_str('1.0.6.1.14 修改姓名影响热门用户列表  success')
							self.write_email_log('1.0.6.1.14 ','修改姓名影响热门用户列表','success')
						else:
							self.write_str('1.0.6.1.14 修改姓名影响热门用户列表 fail')
							self.write_email_log('1.0.6.1.14 ','修改姓名影响热门用户列表','fail')

						#判断用户头像修改是否成功修改热门用户
						print(carousels_user[x]['icon'])
						print(userNewIcon)
						if carousels_user[x]['icon'] ==userNewIcon:
							self.write_str('1.0.6.2.14 修改头像影响热门用户列表  success')
							self.write_email_log('1.0.6.2.14 ','修改头像影响热门用户列表','success')
						else:
							self.write_str('1.0.6.2.14 修改头像影响热门用户列表 fail')
							self.write_email_log('1.0.6.2.14 ','修改头像影响热门用户列表','fail')

			else:
				self.write_str('1.0.6.4 热门用户接口数据返回空 fail')
				self.write_email_log('1.0.6.4 ','热门用户接口数据返回空','fail')
			

		#结束测试
		self.close_fd()
		self.EndTest()		

def  main():
	reload(sys)
	sys.setdefaultencoding='utf-8'

	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case = UserInfo(server,serve_yy,'six')
	case.runUserInfo(persons)

if __name__ == '__main__':
	main()