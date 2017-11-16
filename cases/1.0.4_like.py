# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/1/19
# ----------------------

import os
import sys

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)
import inifile
import time


class Like(Common):

    def __init__(self,server,serve_yy,ModuleName):
        Common.__init__(self,server,serve_yy,ModuleName)

    def run_cases(self,persons):
        isRunTag = False
        isRunLike =False
        isRunClub =False 
        
        result = self.get_mediaId()
        mediaId = int(result)
        print(mediaId)
        if  mediaId != '':
            isRunLike = True
            pass
            
        userId=self.get_pid()
        pid=int(userId)

        mediaIds =[mediaId]
        # ===== 点赞部分 =====
        if isRunLike:

          # # 点赞之前,影响登录用户查看首页列表 
            # ========================================== 2 ========================================
            isFollowListEnd = self.ants_fllowList(pid,1,persons[1])
            print(isFollowListEnd)
            if isFollowListEnd == False:
                #添加关注
                self.ants_follow(pid,1,persons[1])

            time.sleep(5)
            result_find_like_init = self.ants_index('mediaId',mediaId,'likes',persons[1])  

            # # 点赞之前,影响登录用户查看媒体详情 
            # ========================================== 3 ========================================
            mediaInfo_init = self.ants_media_detail(mediaId,persons[1])
            likes_init = mediaInfo_init[0]['likes']
            islike_init = mediaInfo_init[0]['islike']

            #获取tag信息
            tags = mediaInfo_init[0]['tags']
            if tags != '':
                tagIds=tags.split(",")
                tagId=tagIds[0]
                isRunTag = True
                print('tagId:'+str(tagId))

            #获取club信息   
            tagList_init = mediaInfo_init[0]['tagList']
            for x in range(len(tagList_init)):
                if tagList_init[x]['mediaSpecial'] == 10:
                    clubId=tagList_init[x]['id']
                    isRunClub =True
                    print('clubId:'+str(clubId))

            # # 点赞之前,标签最新列表
            # ========================================= 4 =========================================
            if isRunTag:
                result_tag_init = self.ants_tags_least(tagId,'mediaId',mediaId,'likes',persons[1])

            # # 点赞之前,影响登录用户查看个人信息列表 
            # ========================================= 5 =========================================
            result_login_info_likes_init = self.ants_get_user_info(persons[1],'likes',persons[1])


            # # 点赞之前,影响俱乐部最新列表
            # ========================================= 6 =========================================
            if isRunClub:
                likes_club_init = self.ants_club_latest(clubId,'mediaId',mediaId,'likes',persons[1])
                isLike_club_init = self.ants_club_latest(clubId,'mediaId',mediaId,'islike',persons[1])

            # # 点赞之前，影响媒体发布用户查看个人分享列表 
            # ========================================= 7 =========================================
            result_private_share_init = self.ants_private_share(pid,'mediaId',mediaId,'likes',persons[1])
            
            #点赞前，获取用户的消息状态
            like_msgStatus_init = self.ants_get_msgStatus(pid)

        if isRunLike: 
            # # 粉丝点赞
            like_time1=self.get_now_time()
            # 点赞
            bodys = {}
            bodys['mediaId'] = mediaId
            bodys['doLike'] = True
            likeStatus=self.ants_like(mediaId,bodys,persons[1])
            like_time2=self.get_now_time()
            if likeStatus=='success':
                self.write_str(u"1.0.4_1 点赞 success,耗时"+str(self.get_time_long(like_time1,like_time2)))
                self.write_email_log(u"1.0.4_1 ","点赞,耗时"+str(self.get_time_long(like_time1,like_time2)),"success")
            else:
                self.write_str(u"1.0.4_1 点赞 fail")
                self.write_email_log(u"1.0.4_1 ","点赞","fail")

            time.sleep(5)
        if isRunLike:
            # 点赞之后,影响登录用户的喜欢列表 
            # =============================================== 1 ===================================
            likeList_time1=self.get_now_time()
            result_like = self.ants_likeList(persons[1],'mediaId',mediaId,'mediaId',persons[1])
            print(result_like)
            likeList_time2=self.get_now_time()
            if result_like == -1 or result_like == -100:
                self.write_str(u"1.0.4-1.1 点赞之后,登录用户的喜欢列表异常 fail")
                self.write_email_log(u"1.0.4-1.1"," 点赞之后,登录用户的喜欢列表异常","fail")
            elif result_like == False:
                self.write_str(u"1.0.4-1.1 点赞之后,影响登录用户的喜欢列表 fail")
                self.write_email_log(u"1.0.4-1.1"," 点赞之后,影响登录用户的喜欢列表","fail")
            elif result_like[0] ==mediaId:
                self.write_str(u"1.0.4-1.1 点赞之后,影响登录用户的喜欢列表 success,耗时"+str(self.get_time_long(likeList_time1,likeList_time2)))
                self.write_email_log(u"1.0.4-1.1"," 点赞之后,影响登录用户的喜欢列表,耗时"+str(self.get_time_long(likeList_time1,likeList_time2)),"success")
            else:
                self.write_str(u"1.0.4-1.1 点赞之后,影响登录用户的喜欢列表 fail")
                self.write_email_log(u"1.0.4-1.1"," 点赞之后,影响登录用户的喜欢列表","fail")
            
            # # 点赞之后,影响首页列表 
            # ================================================ 2 ===================================
            like_find_time1=self.get_now_time()
            result_find_like = self.ants_index('mediaId',mediaId,'likes',persons[1])
            result_find_isLike = self.ants_index('mediaId',mediaId,'islike',persons[1])
            print(str(result_find_like)+'==='+str(result_find_like_init)+'==='+str(result_find_isLike))
            like_find_time2=self.get_now_time()
            if result_find_like == -1 or result_find_like ==-100:
                self.write_str(u"1.0.4-1.2 点赞之后,登录用户查看首页列表异常 error")
                self.write_email_log(u"1.0.4-1.2"," 点赞之后,登录用户查看首页列表异常","error")
            elif result_find_like== False:
                self.write_str(u"1.0.4-1.2 点赞之后,影响登录用户查看首页列表 fail")
                self.write_email_log(u"1.0.4-1.2"," 点赞之后,影响登录用户查看首页列表","fail")
            elif result_find_like[0]==(result_find_like_init[0]+1) and result_find_isLike ==[1]:
                self.write_str(u"1.0.4-1.2 点赞之后,影响登录用户查看首页列表 success,耗时"+str(self.get_time_long(like_find_time1,like_find_time2)))
                self.write_email_log(u"1.0.4-1.2"," 点赞之后,影响登录用户查看首页列表,耗时"+str(self.get_time_long(like_find_time1,like_find_time2)),"success")
            else:
                self.write_str(u"1.0.4-1.2 点赞之后,影响登录用户查看首页列表 fail")
                self.write_email_log(u"1.0.4-1.2"," 点赞之后,影响登录用户查看首页列表","fail")

            # # 点赞之后,影响登录用户查看媒体详情 
            # ================================================ 3 ===================================
            like_detail_time1=self.get_now_time()
            code_status = self.ants_media_detail(mediaId,persons[1])
            print(code_status)
            if code_status == -1 or code_status == -100:
                self.write_str(u"1.0.4-1.3 点赞之后,登录用户查看媒体详情异常 error")
                self.write_email_log(u"1.0.4-1.3"," 点赞之后,登录用户查看媒体详情异常","error")
            else:
                like_detail_time2 =self.get_now_time()
                likes = code_status[0]['likes']
                islike = code_status[0]['islike']
                if likes==(likes_init+1) and islike==1:
                    self.write_str(u"1.0.4-1.3 点赞之后,影响登录用户查看媒体详情 success,耗时"+str(self.get_time_long(like_detail_time1,like_detail_time2)))
                    self.write_email_log(u"1.0.4-1.3"," 点赞之后,影响登录用户查看媒体详情,耗时"+str(self.get_time_long(like_detail_time1,like_detail_time2)),"success")
                else:
                    self.write_str(u"1.0.4-1.3 点赞之后,影响登录用户查看媒体详情 fail")
                    self.write_email_log(u"1.0.4-1.3"," 点赞之后,影响登录用户查看媒体详情","fail")

            # # 点赞之后,影响标签最新列表
            # ================================================ 4 ====================================
            if isRunTag:
                like_indexFollow_time1=self.get_now_time()
                result_tag = self.ants_tags_least(tagId,'mediaId',mediaId,'likes',persons[1])
                result_tag_isLike = self.ants_tags_least(tagId,'mediaId',mediaId,'islike',persons[1])
                print(str(result_tag)+'==='+str(result_tag_isLike))
                like_indexFollow_time2=self.get_now_time()
                if result_tag == -1 or result_tag == -100:
                    self.write_str(u"1.0.4-1.4 点赞之后,标签最新列表异常 error")
                    self.write_email_log(u"1.0.4-1.4"," 点赞之后,标签最新列表异常","error")
                elif result_tag == False:
                    self.write_str(u"1.0.4-1.4 点赞之后,影响标签最新列表 fail")
                    self.write_email_log(u"1.0.4-1.4"," 点赞之后,影响标签最新列表","fail")
                elif result_tag[0]==(result_tag_init[0]+1) and result_tag_isLike[0] ==1:
                    self.write_str(u"1.0.4-1.4 点赞之后,影响标签最新列表 success,耗时"+str(self.get_time_long(like_indexFollow_time1,like_indexFollow_time2)))
                    self.write_email_log(u"1.0.4-1.4"," 点赞之后,影响标签最新列表,耗时"+str(self.get_time_long(like_indexFollow_time1,like_indexFollow_time2)),"success")
                else:
                    self.write_str(u"1.0.4-1.4 点赞之后,影响标签最新列表 fail")
                    self.write_email_log(u"1.0.4-1.4"," 点赞之后,影响标签最新列表","fail")


            # 点赞之后,影响登录用户查看个人信息列表 
            # =============================================== 5 =====================================
            like_userInfo_time1 =self.get_now_time()
            result_login_info_likes = self.ants_get_user_info(persons[1],'likes',persons[1])
            like_userInfo_time2 =self.get_now_time()
            if result_login_info_likes == -1 or result_login_info_likes == -100:
                self.write_str(u"1.0.4-1.5 点赞之后,登录用户查看个人信息列表异常 error")
                self.write_email_log(u"1.0.4-1.5"," 点赞之后,登录用户查看个人信息列表异常","error")
            elif result_login_info_likes == (result_login_info_likes_init+1):
                self.write_str(u"1.0.4-1.5 点赞之后,影响登录用户查看个人信息列表 success,耗时"+str(self.get_time_long(like_userInfo_time1,like_userInfo_time2)))
                self.write_email_log(u"1.0.4-1.5"," 点赞之后,影响登录用户查看个人信息列表,耗时"+str(self.get_time_long(like_userInfo_time1,like_userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.4-1.5 点赞之后,影响登录用户查看个人信息列表 fail")
                self.write_email_log(u"1.0.4-1.5"," 点赞之后,影响登录用户查看个人信息列表","fail")

            
            # # 点赞,影响俱乐部最新列表 
            # =============================================== 7 =====================================
            if isRunClub:
                cn_city_time1=self.get_now_time()
                likes_club = self.ants_club_latest(clubId,'mediaId',mediaId,'likes',persons[1])
                isLike_club = self.ants_club_latest(clubId,'mediaId',mediaId,'islike',persons[1])
                cn_city_time2 =self.get_now_time()
                if likes_club == -1 or likes_club == -100:
                    self.write_str(u"1.0.4-1.6 点赞之后,俱乐部最新列表异常 error")
                    self.write_email_log(u"1.0.4-1.6"," 点赞之后,俱乐部最新列表异常","error")
                elif likes_club == False:
                    self.write_str(u"1.0.4-1.6 点赞之后,影响俱乐部最新列表 fail")
                    self.write_email_log(u"1.0.4-1.6"," 点赞之后,影响俱乐部最新列表","fail")
                elif likes_club[0]==(likes_club_init[0]+1) and isLike_club[0] ==1:
                    self.write_str(u"1.0.4-1.6 点赞之后,影响俱乐部最新列表 success,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)))
                    self.write_email_log(u"1.0.4-1.6"," 点赞之后,影响俱乐部最新列表,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)),"success")
                else:
                    self.write_str(u"1.0.4-1.6 点赞之后,影响俱乐部最新列表 fail")
                    self.write_email_log(u"1.0.4-1.6"," 点赞之后,影响俱乐部最新列表","fail")

            # # 点赞,影响媒体发布用户查看个人分享列表 
            # =============================================== 8 ======================================
            like_private_time1 =self.get_now_time()
            result_private_share = self.ants_private_share(pid,'mediaId',mediaId,'likes',persons[1])
            like_private_time2 = self.get_now_time()
            if result_private_share == -1 or result_private_share == -100:
                self.write_str(u"1.0.4-1.7 点赞之后,媒体发布用户查看个人分享列表异常 error")
                self.write_email_log(u"1.0.4-1.7"," 点赞之后,媒体发布用户查看个人分享列表异常","error")
            elif result_private_share == False:
                self.write_str(u"1.0.4-1.7 点赞之后,影响媒体发布用户查看个人分享列表 fail")
                self.write_email_log(u"1.0.4-1.7"," 点赞之后,影响媒体发布用户查看个人分享列表","fail")
            elif result_private_share[0] == (result_private_share_init[0]+1):
                self.write_str(u"1.0.4-1.7 点赞之后,影响媒体发布用户查看个人分享列表 success,耗时"+str(self.get_time_long(like_private_time1,like_private_time2)))
                self.write_email_log(u"1.0.4-1.7"," 点赞之后,影响媒体发布用户查看个人分享列表,耗时"+str(self.get_time_long(like_private_time1,like_private_time2)),"success")
            else:
                self.write_str(u"1.0.4-1.7 点赞之后,影响媒体发布用户查看个人分享列表 fail")
                self.write_email_log(u"1.0.4-1.7","点赞之后,影响媒体发布用户查看个人分享列表","fail")

            # # 点赞之后,影响媒体发布用户查看消息状态 
            # =============================================== 9 ======================================
            like_msg_time1=self.get_now_time()
            like_msgStatus = self.ants_get_msgStatus(pid)
            like_msg_time2=self.get_now_time()
            if like_msgStatus == -1 or like_msgStatus == -100:
                self.write_str(u"1.0.4-1.8-1 点赞之后,影响媒体发布用户查看消息状态出现异常 error")
                self.write_email_log(u"1.0.4-1.8-1"," 点赞之后,影响媒体发布用户查看消息状态出现异常","error")
            elif like_msgStatus == False:
                self.write_str(u"1.0.4-1.8-1 点赞之后,影响媒体发布用户查看消息状态 fail")
                self.write_email_log(u"1.0.4-1.8-1"," 点赞之后,影响媒体发布用户查看消息状态","fail")
            elif like_msgStatus[0]['likeCnt']==like_msgStatus_init[0]['likeCnt']+1:
                self.write_str(u"1.0.4-1.8-1 点赞之后,影响媒体发布用户查看消息状态 success")
                self.write_email_log(u"1.0.4-1.8-1"," 点赞之后,影响媒体发布用户查看消息状态","success")
            else:
                self.write_str(u"1.0.4-1.8-1 点赞之后,影响媒体发布用户查看消息状态 fail")
                self.write_email_log(u"1.0.4-1.8-1"," 点赞之后,影响媒体发布用户查看消息状态","fail")

            # # 点赞之后,影响媒体发布用户查看消息列表 
            # =============================================== 9 ======================================
            like_msg_time1=self.get_now_time()
            ax ={}
            isResultMediaGetlist = self.ants_get_msg(mediaId,3,5,persons[1],ax,pid)
            like_msg_time2=self.get_now_time()
            if isResultMediaGetlist == -1 or isResultMediaGetlist == -100:
                self.write_str(u"1.0.4-1.8 点赞之后,影响媒体发布用户查看消息列表出现异常 error")
                self.write_email_log(u"1.0.4-1.8"," 点赞之后,影响媒体发布用户查看消息列表出现异常","error")
            elif isResultMediaGetlist == False:
                self.write_str(u"1.0.4-1.8 点赞之后,影响媒体发布用户查看消息列表 fail")
                self.write_email_log(u"1.0.4-1.8"," 点赞之后,影响媒体发布用户查看消息列表","fail")
            else:
                self.write_str(u"1.0.4-1.8 点赞之后,影响媒体发布用户查看消息列表 success,耗时"+str(self.get_time_long(like_msg_time1,like_msg_time2)))
                self.write_email_log(u"1.0.4-1.8"," 点赞之后,影响媒体发布用户查看消息列表,耗时"+str(self.get_time_long(like_msg_time1,like_msg_time2)),"success")
       
        if isRunLike:
            # 取消点赞 ##############################################
            cel_like_time1=self.get_now_time()
            #取消点赞
            bodys['doLike'] = False
            dislikeStatus=self.ants_like(mediaId,bodys,persons[1])
            cel_like_time2=self.get_now_time()
            if dislikeStatus=='success':
                self.write_str("1.0.4_2 取消点赞success,耗时"+str(self.get_time_long(cel_like_time1,cel_like_time2)))
                self.write_email_log(u"1.0.4_2"," 取消点赞,耗时"+str(self.get_time_long(cel_like_time1,cel_like_time2)),"success")
            else:
                self.write_email_log(u"1.0.4_2"," 取消点赞","fail")

            time.sleep(5)

        if isRunLike:        
            # 取消点赞之后, 影响登录用户的喜欢列表 
            # ======================================= 1 ============================================
            likeList_time3=self.get_now_time()
            result_like_end = self.ants_likeList(persons[1],'mediaId',mediaId,'mediaId',persons[1])
            print(result_like_end)
            likeList_time4=self.get_now_time()
            if result_like_end == False:
                self.write_str(u"1.0.4-2.1 取消点赞之后,影响登录用户的喜欢列表 success,耗时"+str(self.get_time_long(likeList_time3,likeList_time4)))
                self.write_email_log(u"1.0.4-2.1"," 取消点赞之后,影响登录用户的喜欢列表,耗时"+str(self.get_time_long(likeList_time3,likeList_time4)),"success")
            else:
                self.write_str(u"1.0.4-2.1 取消点赞之后,影响登录用户的喜欢列表 fail")
                self.write_email_log(u"1.0.4-2.1"," 取消点赞之后,影响登录用户的喜欢列表","fail")

            # # 取消点赞之后,影响登录用户查看首页列表 
            # ======================================= 2 ============================================
            like_find_time3=self.get_now_time()
            result_find_like_end = self.ants_index('mediaId',mediaId,'likes',persons[1])
            result_find_isLike_end = self.ants_index('mediaId',mediaId,'islike',persons[1])
            print(result_find_like)
            print(result_find_like_end)
            print(result_find_isLike_end)
            like_find_time4=self.get_now_time()
            if result_find_like_end ==-1 or result_find_like_end==-100:
                self.write_str(u"1.0.4-2.2 取消点赞之后,登录用户查看首页列表异常 error")
                self.write_email_log(u"1.0.4-2.2"," 取消点赞之后,登录用户查看首页列表异常","error")
            elif result_find_like_end == False:
                self.write_str(u"1.0.4-2.2 取消点赞之后,影响登录用户查看首页列表 fail")
                self.write_email_log(u"1.0.4-2.2"," 取消点赞之后,影响登录用户查看首页列表","fail")
            elif result_find_like[0]==(result_find_like_end[0]+1) and result_find_isLike_end == [0]:
                self.write_str(u"1.0.4-2.2 取消点赞之后,影响登录用户查看首页列表 success,耗时"+str(self.get_time_long(like_find_time3,like_find_time4)))
                self.write_email_log(u"1.0.4-2.2"," 取消点赞之后,影响登录用户查看首页列表,耗时"+str(self.get_time_long(like_find_time3,like_find_time4)),"success")
            else:
                self.write_str(u"1.0.4-2.2 取消点赞之后,影响登录用户查看首页列表 fail")
                self.write_email_log(u"1.0.4-2.2"," 取消点赞之后,影响登录用户查看首页列表","fail")

            # # 取消点赞之后,影响登录用户查看媒体详情 
            # ======================================= 3 =============================================
            like_detail_time3=self.get_now_time()
            code_status_end = self.ants_media_detail(mediaId,persons[1])
            like_detail_time4=self.get_now_time()
            likes_end = code_status_end[0]['likes']
            islike_end = code_status_end[0]['islike']
            if likes==(likes_end+1) and islike_end==0:
                self.write_str(u"1.0.4-2.3 取消点赞之后,影响登录用户查看媒体详情 success,耗时"+str(self.get_time_long(like_detail_time3,like_detail_time4)))
                self.write_email_log(u"1.0.4-2.3"," 取消点赞之后,影响登录用户查看媒体详情,耗时"+str(self.get_time_long(like_detail_time3,like_detail_time4)),"success")
            else:
                self.write_str(u"1.0.4-2.3 取消点赞之后,影响登录用户查看媒体详情 fail")
                self.write_email_log(u"1.0.4-2.3"," 取消点赞之后,影响登录用户查看媒体详情","fail")

            # # 取消点赞之后,影响标签最新列表 
            # ======================================= 4 =============================================
            if isRunTag:
                like_indexFollow_time3=self.get_now_time()
                result_tag_end = self.ants_tags_least(tagId,'mediaId',mediaId,'likes',persons[1])
                result_tag_isLike_end = self.ants_tags_least(tagId,'mediaId',mediaId,'islike',persons[1])
                like_indexFollow_time4=self.get_now_time()
                if result_tag[0]==(result_tag_end[0]+1) and result_tag_isLike_end==[0]:
                    self.write_str(u"1.0.4-2.4 取消点赞之后,影响标签最新列表 success,耗时"+str(self.get_time_long(like_indexFollow_time3,like_indexFollow_time4)))
                    self.write_email_log(u"1.0.4-2.4"," 取消点赞之后,影响标签最新列表,耗时"+str(self.get_time_long(like_indexFollow_time3,like_indexFollow_time4)),"success")
                else:
                    self.write_str(u"1.0.4-2.4 取消点赞之后,影响标签最新列表 fail") 
                    self.write_email_log(u"1.0.4-2.4"," 取消点赞之后,影响标签最新列表","fail")

            # 取消点赞之后,影响登录用户查看个人信息列表 
            # ======================================= 5 =============================================
            like_userInfo_time3=self.get_now_time()
            result_login_info_likes_end = self.ants_get_user_info(persons[1],'likes',persons[1])
            like_userInfo_time4=self.get_now_time()
            if result_login_info_likes_end == -1 or result_login_info_likes_end == -100:
                self.write_str(u"1.0.4-2.5 取消点赞之后,登录用户查看个人信息列表异常 error")
                self.write_email_log(u"1.0.4-2.5"," 取消点赞之后,登录用户查看个人信息列表异常","error")
            elif result_login_info_likes == (result_login_info_likes_end+1):
                self.write_str(u"1.0.4-2.5 取消点赞之后,影响登录用户查看个人信息列表 success,耗时"+str(self.get_time_long(like_userInfo_time3,like_userInfo_time4)))
                self.write_email_log(u"1.0.4-2.5"," 取消点赞之后,影响登录用户查看个人信息列表,耗时"+str(self.get_time_long(like_userInfo_time3,like_userInfo_time4)),"success")
            else:
                self.write_str(u"1.0.4-2.5 取消点赞之后,影响登录用户查看个人信息列表 fail")
                self.write_email_log(u"1.0.4-2.5"," 取消点赞之后,影响登录用户查看个人信息列表","fail")

            # # 点赞,影响俱乐部最新列表 
            # =============================================== 7 =====================================
            if isRunClub:
                cn_city_time1=self.get_now_time()
                likes_club_end = self.ants_club_latest(clubId,'mediaId',mediaId,'likes',persons[1])
                isLike_club_end = self.ants_club_latest(clubId,'mediaId',mediaId,'islike',persons[1])
                cn_city_time2 =self.get_now_time()
                print(str(likes_club_end)+'==='+str(likes_club)+'==='+str(isLike_club_end))
                if likes_club[0]==(likes_club_end[0]+1) and isLike_club_end ==[0]:
                    self.write_str(u"1.0.4-2.6 取消点赞之后,影响俱乐部最新列表 success,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)))
                    self.write_email_log(u"1.0.4-2.6"," 取消点赞之后,影响俱乐部最新列表,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)),"success")
                else:
                    self.write_str(u"1.0.4-2.6 取消点赞之后,影响俱乐部最新列表 fail")
                    self.write_email_log(u"1.0.4-2.6"," 取消点赞之后,影响俱乐部最新列表","fail")

            # # 取消点赞之后,影响媒体发布用户查看个人分享列表 
            # ======================================= 8 ==============================================
            like_private_time3=self.get_now_time()
            result_private_share_end = self.ants_private_share(pid,'mediaId',mediaId,'likes',persons[1])
            like_private_time4=self.get_now_time()
            if result_private_share[0] == (result_private_share_end[0]+1):
                self.write_str(u"1.0.4-2.7 取消点赞之后,影响媒体发布用户查看个人分享列表 success,耗时"+str(self.get_time_long(like_private_time3,like_private_time4)))
                self.write_email_log(u"1.0.4-2.7"," 取消点赞之后,影响媒体发布用户查看个人分享列表,耗时"+str(self.get_time_long(like_private_time3,like_private_time4)),"success")
            else:
                self.write_str(u"1.0.4-2.7 取消点赞之后,影响媒体发布用户查看个人分享列表 fail")
                self.write_email_log(u"1.0.4-2.7 ","取消点赞之后,影响媒体发布用户查看个人分享列表","fail")
            
            # # 取消点赞之后,影响媒体发布用户查看消息列表 
            # ====================================== 9 ================================================
            like_msg_time5=self.get_now_time()
            ax ={}
            isResultMediaGetlistEnd = self.ants_get_msg(mediaId,3,5,persons[1],ax,pid)
            print(isResultMediaGetlistEnd)
            like_msg_time6=self.get_now_time()
            if isResultMediaGetlistEnd == -1 or isResultMediaGetlistEnd == -100:
                self.write_str(u"1.0.4-2.8 取消点赞之后,媒体发布用户查看消息列表出现异常 error")
                self.write_email_log(u"1.0.4-2.8"," 取消点赞之后,媒体发布用户查看消息列表出现异常","error")
            elif isResultMediaGetlistEnd == False:
                self.write_str(u"1.0.4-2.8 取消点赞之后,影响媒体发布用户查看消息列表 success,耗时"+str(self.get_time_long(like_msg_time5,like_msg_time6)))
                self.write_email_log(u"1.0.4-2.8"," 取消点赞之后,影响媒体发布用户查看消息列表,耗时"+str(self.get_time_long(like_msg_time5,like_msg_time6)),"success")
            else:
                self.write_str(u"1.0.4-2.8 取消点赞之后,影响媒体发布用户查看消息列表 fail")
                self.write_email_log(u"1.0.4-2.8"," 取消点赞之后,影响媒体发布用户查看消息列表","fail")

            #取消关注
            self.ants_follow(pid,0,persons[1])

        # # 结束测试
        self.close_fd()
        self.EndTest()



def main():
    reload(sys)

    
    server,persons,serve_yy,server_firmware = inifile.get_input_params()
    cases = Like(server,serve_yy,"four")
    cases.run_cases(persons)


if __name__=="__main__":
    main()