# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/5/22
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0]
# scriptpath=os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile

class live(Common):
	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)

	def runCase(self,persons):
		self.write_str("===========直播============")
		self.write_email_log('0000',"===========直播============","success")

		# 发布影响个人信息列表===========1.0.1——1======================
		userInfo_liveCount_init = self.ants_get_user_info(persons[0],'liveCount',persons[0]) 


		#获取直播上传url地址==========1.0.13-1===================
		media ='mao.jpg'
		fileId,mediaUrl,thumbUrl,uploadMethod = self.ants_get_media_fileId(2,persons[0])

		if fileId != '':
			# 完成媒体上传,五
			media = 'mao.jpg'
			thumb = 'mao.jpg'
			result=''
			for x in range(1,5):
				publish_time3 =self.get_now_time()
				isUpLoad = self.ants_upload_local_video_work(mediaUrl,media,thumbUrl,thumb)
				publish_time4 =self.get_now_time()
				if isUpLoad ==True:
					print(isUpLoad)
					self.write_str(u"1.0.13-0 第"+str(x)+"次上传视频 success,耗时：")
					self.write_email_log(u"1.0.13-0 ","第"+str(x)+"次上传视频耗时：",'success')

					#创建者直播================1.0.13-2===================
					bodys = {}
					bodys['title'] = 'live_test'
					bodys['type'] = 1
					bodys['media_memo'] = 'live trumb upload test'
					bodys['width'] = 1000
					bodys['height'] = 1000
					bodys['file_id'] = '230916ee6b636f862a78e482e1bae97bc7bd60'
					bodys['media_url'] = 'http://live.weibo.com/show?id=1042097:ee6b636f862a78e482e1bae97bc7bd60'
					bodys['visits'] = 0
					bodys['thumbnail_id'] = fileId
					bodys['view'] = 'HSL'

					liveId = self.ants_open_live(bodys,persons[0])
					#liveId='4b8cbad083a5429c91746906509308e4'
					if liveId != 0:
						self.write_str(u"1.0.13-1 创建直播 success")
						self.write_email_log(u"1.0.13-1 ","创建直播,",'success')
						isRunLive =True
					else:
						self.write_str(u"1.0.13-1 创建直播 fail")
						self.write_email_log(u"1.0.13-1 ","创建直播",'fail')
					break
				else:
					self.write_str(u"1.0.13-0 第"+str(x)+"次上传视频 fail")
					self.write_email_log(u"1.0.13-0 ","第"+str(x)+"次上传视频",'fail')
					continue
		
		#获取直播详情====================1.0.13-2=============	
		if isRunLive:
			live_detail = self.ants_live_detail(liveId,persons[0])
			print(live_detail)
			if live_detail ==-1 or live_detail ==-100:
				self.write_str(u"1.0.13-2 创建直播后，直播详情展示异常 error")
				self.write_email_log(u"1.0.13-2 ","创建直播后，直播详情展示异常","error")
			elif live_detail[0]['status'] == 0:
				self.write_str(u"1.0.13-2 创建直播后，直播详情 success")
				self.write_email_log(u"1.0.13-2 ","创建直播后，直播详情","success")
			else:
				self.write_str(u"1.0.13-2 创建直播后，直播详情 fail")
				self.write_email_log(u"1.0.13-2 ","创建直播后，直播详情","fail")

			#=============个人直播列表============================
			psersonal_live = self.ants_personal_live(liveId,persons[0])
			if psersonal_live ==-1 or psersonal_live==-100:
				self.write_str(u"1.0.13-3 创建直播后，个人直播列表展示异常 error")
				self.write_email_log(u"1.0.13-3 ","创建直播后，个人直播列表展示异常","error")
			elif psersonal_live == False:
				self.write_str(u"1.0.13-3 创建直播后，个人直播列表展示 fail")
				self.write_email_log(u"1.0.13-3 ","创建直播后，个人直播列表展示","fail")
			else:
				self.write_str(u"1.0.13-3 创建直播后，个人直播列表展示 success")
				self.write_email_log(u"1.0.13-3 ","创建直播后，个人直播列表展示","success")

			#=============直播列表,type=0最新，type=1 最热============================
			live_list = self.ants_live_list(0,liveId,'status',persons[0])
			if live_list ==-1 or live_list==-100:
				self.write_str(u"1.0.13-4 创建直播后，最新直播列表展示异常 error")
				self.write_email_log(u"1.0.13-4 ","创建直播后，最新直播列表展示异常","error")
			elif live_list == False:
				self.write_str(u"1.0.13-4 创建直播后，最新直播列表展示 fail")
				self.write_email_log(u"1.0.13-4 ","创建直播后，最新直播列表展示","fail")
			else:
				self.write_str(u"1.0.13-4 创建直播后，最新直播列表展示 success")
				self.write_email_log(u"1.0.13-4 ","创建直播后，最新直播列表展示","success")

			# 发布影响个人信息列表===========1.0.1——1======================
			userInfo_liveCount = self.ants_get_user_info(persons[0],'liveCount',persons[0])
			if userInfo_liveCount == -1 or userInfo_liveCount == -100:
				self.write_str(u"1.0.13-5 创建直播后，用户个人信息列表内liveCount展示异常 error")
				self.write_email_log(u"1.0.13-5 ","创建直播后，用户个人信息列表内liveCount展示异常","error")
			elif userInfo_liveCount == userInfo_liveCount_init+1:
				self.write_str(u"1.0.13-5 创建直播后，用户个人信息列表内liveCount展示 success")
				self.write_email_log(u"1.0.13-5 ","创建直播后，用户个人信息列表内liveCount展示","success")
			else:
				self.write_str(u"1.0.13-5 创建直播后，用户个人信息列表内liveCount展示 fail")
				self.write_email_log(u"1.0.13-5 ","创建直播后，用户个人信息列表内liveCount展示","fail")
					
			#============评论前，直播评论列表=========
			comList_init=self.ants_liveComment_list(liveId,persons[0])
			print(comList_init)


			#=============直播添加评论============================
			bodys_liveCom = {}
			bodys_liveCom['mediaId'] = liveId
			bodys_liveCom['content'] = 'live=====comment==='
			add_liveComment = self.ants_add_liveComment(bodys_liveCom,persons[0])

			if add_liveComment == 'success':
				self.write_str(u"1.0.13-6 直播内添加评论 success")
				self.write_email_log(u"1.0.13-6 ","直播内添加评论","success")

				#============直播评论列表=========
				comList=self.ants_liveComment_list(liveId,persons[0])
				print(comList)
				if comList == -1 or comList ==-100:
					self.write_str(u"1.0.13-6.1 添加直播评论后，直播评论列表异常 error")
					self.write_email_log(u"1.0.13-6.1 ","添加直播评论后，直播评论列表异常","error")
				elif len(comList) == len(comList_init)+1:
					self.write_str(u"1.0.13-6.1 添加直播评论后，直播评论列表展示 success")
					self.write_email_log(u"1.0.13-6.1 ","添加直播评论后，直播评论列表展示","success")
				else:
					self.write_str(u"1.0.13-6.1 添加直播评论后，直播评论列表展示 fail")
					self.write_email_log(u"1.0.13-6.1 ","添加直播评论后，直播评论列表展示","fail")
			else:
				self.write_str(u"1.0.13-6 直播内添加评论 fail")
				self.write_email_log(u"1.0.13-6 ","直播内添加评论","fail")

			#点赞列表init=======
			likeList_init=self.ants_liveLike_list(liveId,persons[0])
			print(likeList_init)

			#=======获取直播详情=============
			live_detail_like_init = self.ants_live_detail(liveId,persons[0])
			print(live_detail_like_init)

			#=============直播点赞============================
			bodys_live_like = {}
			bodys_live_like['mediaId'] = liveId
			bodys_live_like['num'] = 1
			add_liveLike = self.ants_add_liveLike(bodys_live_like,persons[0])

			if add_liveLike == 'success':
				self.write_str(u"1.0.13-7 直播内点赞 success")
				self.write_email_log(u"1.0.13-7 ","直播内点赞","success")

				#============获取直播点赞数和在线人数=========
				likeList=self.ants_liveLike_list(liveId,persons[0])
				print(likeList)
				if likeList == -1 or likeList ==-100:
					self.write_str(u"1.0.13-7.1 点赞直播后，获取直播点赞数和在线人数异常 error")
					self.write_email_log(u"1.0.13-7.1 ","点赞直播后，获取直播点赞数和在线人数异常","error")
				elif likeList[0]['likes'] == likeList_init[0]['likes']+1:
					self.write_str(u"1.0.13-7.1 点赞直播后，获取直播点赞数和在线人数展示 success")
					self.write_email_log(u"1.0.13-7.1 ","点赞直播后，获取直播点赞数和在线人数展示","success")
				else:
					self.write_str(u"1.0.13-7.1 点赞直播后，获取直播点赞数和在线人数展示 fail")
					self.write_email_log(u"1.0.13-7.1 ","点赞直播后，获取直播点赞数和在线人数展示","fail")

				#=======获取直播详情=============
				live_detail_like = self.ants_live_detail(liveId,persons[0])
				print(live_detail_like)
				if live_detail_like ==-1 or live_detail_like ==-100:
					self.write_str(u"1.0.13-7.2 点赞直播后，直播详情展示异常 error")
					self.write_email_log(u"1.0.13-7.2 ","点赞直播后，直播详情展示异常","error")
				elif live_detail_like[0]['likes'] == live_detail_like_init[0]['likes']+1:
					self.write_str(u"1.0.13-7.2 点赞直播后，直播详情likes success")
					self.write_email_log(u"1.0.13-7.2 ","点赞直播后，直播详情likes","success")
				else:
					self.write_str(u"1.0.13-7.2 点赞直播后，直播详情likes fail")
					self.write_email_log(u"1.0.13-7.2 ","点赞直播后，直播详情likes","fail")

			else:
				self.write_str(u"1.0.13-7 直播内点赞 fail")
				self.write_email_log(u"1.0.13-7 ","直播内点赞","fail")

			#==========直播内添加关注====================
			#发布影响我关注的人发布的媒体列表
			isFollowListEnd = self.ants_fllowList(persons[0],1,persons[1])
			print(isFollowListEnd)
			if isFollowListEnd != False:
				#取消关注
				celRE=self.ants_follow(persons[0],0,persons[1])
				if celRE =='success':
					self.write_str(str(persons[1])+"取消关注"+str(persons[0])+" success")
					self.write_email_log('1.0.13-8',str(persons[1])+"取消关注"+str(persons[0]),"success")

            #添加关注
			addRE=self.ants_follow(persons[0],1,persons[1])
			if addRE =='success':
				self.write_str("1.0.13-8 "+str(persons[1])+"添加关注"+str(persons[0])+" success")
				self.write_email_log("1.0.13-8 ",str(persons[1])+"添加关注"+str(persons[0]),"success")

				#==============获取直播详情=====================
				live_detail_follow_init = self.ants_live_detail(liveId,persons[1])
				print(live_detail_follow_init)
				if live_detail_follow_init ==-1 or live_detail_follow_init ==-100:
					self.write_str(u"1.0.13-8.1 添加关注后，直播详情展示异常 error")
					self.write_email_log(u"1.0.13-8.1 ","添加关注后，直播详情展示异常","error")
				elif live_detail_follow_init[0]['isFollow'] == 1:
					self.write_str(u"1.0.13-8.1 添加关注后，直播详情isFollow展示 success")
					self.write_email_log(u"1.0.13-8.1 ","添加关注后，直播详情isFollow展示","success")
				else:
					self.write_str(u"1.0.13-8.1 添加关注后，直播详情isFollow展示 fail")
					self.write_email_log(u"1.0.13-8.1 ","添加关注后，直播详情isFollow展示","fail")

				#=============直播列表,type=0最新，type=1 最热============================
				live_list_follow_init = self.ants_live_list(0,liveId,'isFollow',persons[1])
				print(live_list_follow_init)
				if live_list_follow_init ==-1 or live_list_follow_init==-100:
					self.write_str(u"1.0.13-8.2 添加关注后，最新直播列表isFollow展示异常 error")
					self.write_email_log(u"1.0.13-8.2 ","添加关注后，最新直播列表isFollow展示异常","error")
				elif live_list_follow_init[0] == 1:
					self.write_str(u"1.0.13-8.2 添加关注后，最新直播列表isFollow展示 success")
					self.write_email_log(u"1.0.13-8.2 ","添加关注后，最新直播列表isFollow展示","success")
				else:
					self.write_str(u"1.0.13-8.2 添加关注后，最新直播列表isFollow展示 fail")
					self.write_email_log(u"1.0.13-8.2 ","添加关注后，最新直播列表isFollow展示","fail")

				#取消关注
				celRE_end=self.ants_follow(persons[0],0,persons[1])
				if celRE_end =='success':
					self.write_str("1.0.13-8.3 "+str(persons[1])+"取消关注"+str(persons[0])+" success")
					self.write_email_log("1.0.13-8.3 ",str(persons[1])+"取消关注"+str(persons[0]),"success")

                    #==============获取直播详情=====================
					live_detail_follow_end = self.ants_live_detail(liveId,persons[1])
					print(live_detail_follow_end)
					if live_detail_follow_end ==-1 or live_detail_follow_end ==-100:
						self.write_str(u"1.0.13-8.4 取消关注后，直播详情展示异常 error")
						self.write_email_log(u"1.0.13-8.4 ","取消关注后，直播详情展示异常","error")
					elif live_detail_follow_end[0]['isFollow'] == 0:
						self.write_str(u"1.0.13-8.4 取消关注后，直播详情isFollow展示 success")
						self.write_email_log(u"1.0.13-8.4 ","取消关注后，直播详情isFollow展示","success")
					else:
						self.write_str(u"1.0.13-8.4 取消关注后，直播详情isFollow展示 fail")
						self.write_email_log(u"1.0.13-8.4 ","取消关注后，直播详情isFollow展示","fail")

					#=============直播列表,type=0最新，type=1 最热============================
					live_list_follow_end = self.ants_live_list(0,liveId,'isFollow',persons[1])
					print(live_list_follow_end)
					if live_list_follow_end ==-1 or live_list_follow_end==-100:
						self.write_str(u"1.0.13-8.5 取消关注后，最新直播列表isFollow展示异常 error")
						self.write_email_log(u"1.0.13-8.5 ","取消关注后，最新直播列表isFollow展示异常","error")
					elif live_list_follow_end[0] == 0:
						self.write_str(u"1.0.13-8.5 取消关注后，最新直播列表isFollow展示 success")
						self.write_email_log(u"1.0.13-8.5 ","取消关注后，最新直播列表isFollow展示","success")
					else:
						self.write_str(u"1.0.13-8.5 取消关注后，最新直播列表isFollow展示 fail")
						self.write_email_log(u"1.0.13-8.5 ","取消关注后，最新直播列表isFollow展示","fail")
				else:
					self.write_str("1.0.13-8.3 "+str(persons[1])+"取消关注"+str(persons[0])+" fail")
					self.write_email_log("1.0.13-8.3 ",str(persons[1])+"取消关注"+str(persons[0]),"fail")


			#=========修改直播状态========================
			bodys_live_close = {}
			bodys_live_close['mediaId'] = liveId
			bodys_live_close['status'] = 9
			close_result=self.ants_live_close(bodys_live_close,persons[0])
			print(close_result)
			if close_result=='success':
				self.write_str(u"1.0.13-9 删除直播 success")
				self.write_email_log(u"1.0.13-9 ","删除直播","success")
			else:
				self.write_str(u"1.0.13-9 删除直播 fail")
				self.write_email_log(u"1.0.13-9 ","删除直播","fail")

			# 发布影响个人信息列表===========1.0.1——1======================
			userInfo_liveCount_end = self.ants_get_user_info(persons[0],'liveCount',persons[0])
			if userInfo_liveCount_end ==-1 or userInfo_liveCount_end ==-100:
				self.write_str(u"1.0.13-10 删除直播后，用户个人信息列表内liveCount展示异常 error")
				self.write_email_log(u"1.0.13-10 ","删除直播后，用户个人信息列表内liveCount展示异常","error")
			elif userInfo_liveCount_end ==userInfo_liveCount-1:
				self.write_str(u"1.0.13-10 删除直播后，用户个人信息列表内liveCount展示 success")
				self.write_email_log(u"1.0.13-10 ","删除直播后，用户个人信息列表内liveCount展示","success")
			else:
				self.write_str(u"1.0.13-10 删除直播后，用户个人信息列表内liveCount展示 fail")
				self.write_email_log(u"1.0.13-10 ","删除直播后，用户个人信息列表内liveCount展示","fail")

			#==============获取直播详情=====================
			live_detail_end = self.ants_live_detail(liveId,persons[0])
			print(live_detail_end)
			if live_detail_end ==-1 or live_detail_end ==-100:
				self.write_str(u"1.0.13-11 删除直播后，直播详情展示异常 error")
				self.write_email_log(u"1.0.13-11 ","删除直播后，直播详情展示异常","error")
			elif live_detail_end[0]['status'] == 9:
				self.write_str(u"1.0.13-11 删除直播后，直播详情 success")
				self.write_email_log(u"1.0.13-11 ","删除直播后，直播详情","success")
			else:
				self.write_str(u"1.0.13-11 删除直播后，直播详情 fail")
				self.write_email_log(u"1.0.13-11 ","删除直播后，直播详情","fail")

			#=============个人直播列表============================
			psersonal_live_end = self.ants_personal_live(liveId,persons[0])
			if psersonal_live_end ==-1 or psersonal_live_end==-100:
				self.write_str(u"1.0.13-12 删除直播后，个人直播列表展示异常 error")
				self.write_email_log(u"1.0.13-12 ","删除直播后，个人直播列表展示异常","error")
			elif psersonal_live_end == False:
				self.write_str(u"1.0.13-12 删除直播后，个人直播列表展示 success")
				self.write_email_log(u"1.0.13-12 ","删除直播后，个人直播列表展示","success")
			else:
				self.write_str(u"1.0.13-12 删除直播后，个人直播列表展示 fail")
				self.write_email_log(u"1.0.13-12 ","删除直播后，个人直播列表展示","fail")

			#=============直播列表,type=0最新，type=1 最热============================
			live_list_end = self.ants_live_list(0,liveId,'status',persons[0])
			if live_list_end == -1 or live_list_end ==-100:
				self.write_str(u"1.0.13-13 删除直播后，最新直播列表展示异常 error")
				self.write_email_log(u"1.0.13-13 ","删除直播后，最新直播列表展示异常","error")
			elif live_list_end == False:
				self.write_str(u"1.0.13-13 删除直播后，最新直播列表展示 success")
				self.write_email_log(u"1.0.13-13 ","删除直播后，最新直播列表展示","success")
			else:
				self.write_str(u"1.0.13-13 删除直播后，最新直播列表展示 fail")
				self.write_email_log(u"1.0.13-13 ","删除直播后，最新直播列表展示","fail")

def main():
	reload(sys)


	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=live(server,serve_yy,'thirteen')
	case.runCase(persons)

if __name__ == '__main__':
	main()