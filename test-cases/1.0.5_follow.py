# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/1/19
# ----------------------

import os
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)
import inifile
import time

class Follow(Common):

    def __init__(self,server,serve_yy,ModuleName):
        Common.__init__(self,server,serve_yy,ModuleName)

    def run_follow(self,persons):
        RunCase=False
        result = self.get_mediaId()
        mediaId = int(result)
        if mediaId != 0:
            RunCase =True

        userId=self.get_pid()
        pid=int(userId)

        # ============= 添加（取消）关注 =================================
        if RunCase:
            self.write_str("===========添加（取消）关注============")
            self.write_email_log("0000","===========添加（取消）关注============","success")

            #发布影响我关注的人发布的媒体列表
            isFollowListEnd = self.ants_fllowList(pid,1,persons[1])
            print(isFollowListEnd)
            if isFollowListEnd != False:
                #取消关注
                celRE=self.ants_follow(pid,0,persons[1])
                if celRE =='success':
                    self.write_str('1.0.5'+str(persons[1])+"取消关注"+str(pid)+" success")
                    self.write_email_log('1.0.5',str(persons[1])+"取消关注"+str(pid),"success")


            # # 添加关注之前,影响登录用户的个人信息  
            # ============================================= 2 =================================
            result_follows_init = self.ants_get_user_info(persons[1],'follows',persons[1])
            print('result_follows_init:'+str(result_follows_init))
            # # 添加关注之前,影响被关注用户的个人信息 
            # ============================================= 4 =================================
            result_login_info_fans_init = self.ants_get_user_info(pid,'fans',persons[1])
            print('result_login_info_fans_init:'+str(result_login_info_fans_init))

            #添加关注之前，获取用户的消息状态
            follow_msgStatus_init = self.ants_get_msgStatus(pid)

            
            # # 添加关注 ==================================
            add_time1=self.get_now_time()
            isAddFollow = self.ants_follow(pid,1,persons[1])
            add_time2=self.get_now_time()
            print(isAddFollow)
            if isAddFollow == 'success':
                self.write_str(u"1.0.5_1 添加关注 success，耗时"+str(self.get_time_long(add_time1,add_time2)))
                self.write_email_log(u"1.0.5"," 添加关注，耗时"+str(self.get_time_long(add_time1,add_time2)),"success")
            else:
                self.write_str(u"1.0.5_1 添加关注 fail")
                self.write_email_log(u"1.0.5_1"," 添加关注","fail")

            time.sleep(5)

            # # 添加关注之后,影响登录用户的关注列表 
            # ========================================= 1 =====================================
            followList_time1=self.get_now_time()
            isFollowList = self.ants_fllowList(pid,1,persons[1])
            followList_time2=self.get_now_time()
            if isFollowList ==-1 or isFollowList== -100:
                self.write_str(u"1.0.5-1.1 添加关注之后,登录用户的关注列表异常 error")
                self.write_email_log(u"1.0.5-1.1"," 添加关注之后,登录用户的关注列表异常","error")
            elif isFollowList == False:
                self.write_str(u"1.0.5-1.1 添加关注之后,影响登录用户的关注列表 fail")
                self.write_email_log(u"1.0.5-1.1"," 添加关注之后,影响登录用户的关注列表","fail")
            else:
                self.write_str(u"1.0.5-1.1 添加关注之后,影响登录用户的关注列表 success，耗时"+str(self.get_time_long(followList_time1,followList_time2)))
                self.write_email_log(u"1.0.5-1.1 ","添加关注之后,影响登录用户的关注列表，耗时"+str(self.get_time_long(followList_time1,followList_time2)),"success")
            
            # # 添加关注之后,影响登录用户的个人信息 
            # ========================================= 2 =====================================
            userInfo_time1=self.get_now_time()
            result_follows = self.ants_get_user_info(persons[1],'follows',persons[1])
            userInfo_time2=self.get_now_time()
            print(result_follows_init)
            print(result_follows)
            if result_follows==(result_follows_init+1):
                self.write_str(u"1.0.5-1.2 添加关注之后,影响登录用户的个人信息follows success，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.5-1.2 ","添加关注之后,影响登录用户的个人信息follows，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.5-1.2 添加关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-1.2"," 添加关注之后,影响登录用户的个人信息","fail")

            # # 添加关注之后,影响被关注用户的粉丝列表 
            # ========================================= 3 =====================================
            fanList_time1=self.get_now_time()
            isFollowFans = self.ants_get_fanList_isIn(pid,-1,persons[1])
            fanList_time2=self.get_now_time()
            if isFollowFans:
                self.write_str(u"1.0.5-1.3 添加关注之后,影响被关注用户的粉丝列表 success，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)))
                self.write_email_log(u"1.0.5-1.3"," 添加关注之后,影响被关注用户的粉丝列表，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)),"success")
            else:
                self.write_str(u"1.0.5-1.3 添加关注之后,影响被关注用户的粉丝列表 fail")
                self.write_email_log(u"1.0.5-1.3 ","添加关注之后,影响被关注用户的粉丝列表","fail")
            
            # # 添加关注之后,影响被关注用户的个人信息 
            # ========================================= 4 =====================================
            userInfo_time3=self.get_now_time()
            result_login_info_fans = self.ants_get_user_info(pid,'fans',persons[1])
            userInfo_time4=self.get_now_time()
            print(result_login_info_fans_init)
            print(result_login_info_fans)
            if result_login_info_fans==(result_login_info_fans_init+1):
                self.write_str(u"1.0.5-1.4 添加关注之后,影响被关注用户的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                self.write_email_log(u"1.0.5-1.4"," 添加关注之后,影响被关注用户的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
            else:
                self.write_str(u"1.0.5-1.4 添加关注之后,影响被关注用户的个人信息fans fail")
                self.write_email_log(u"1.0.5-1.4"," 添加关注之后,影响被关注用户的个人信息fans","fail")

            # # 添加关注之后,影响登录用户查看被关注用户的媒体详情 
            # ======================================== 5 ======================================
            detail_time1=self.get_now_time()
            reult_share_media_detail = self.ants_media_detail(mediaId,persons[1])
            detail_time2=self.get_now_time()
            reult_share_media_detail_b = reult_share_media_detail[0]['isFollow']
            if reult_share_media_detail_b==1:
                self.write_str(u"1.0.5-1.5 添加关注之后,影响登录用户查看被关注用户的媒体详情 success，耗时"+str(self.get_time_long(detail_time1,detail_time2)))
                self.write_email_log(u"1.0.5-1.5"," 添加关注之后,影响登录用户查看被关注用户的媒体详情，耗时"+str(self.get_time_long(detail_time1,detail_time2)),"success")
            else:
                self.write_str(u"1.0.5-1.5 添加关注之后,影响登录用户查看被关注用户的媒体详情 fail")
                self.write_email_log(u"1.0.5-1.5"," 添加关注之后,影响登录用户查看被关注用户的媒体详情","fail")
            
            # 添加关注之后,影响被关注用户的消息状态 
            # ======================================== 6 =======================================
            follow_msgStatus = self.ants_get_msgStatus(pid)
            if follow_msgStatus == -1 or follow_msgStatus == -100:
                self.write_str(u"1.0.5-1.6 添加关注之后,被关注用户的消息状态异常 error")
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,被关注用户的消息状态出现异常","error")
            elif follow_msgStatus == False:
                self.write_str(u"1.0.5-1.6 添加关注之后,被关注用户的消息状态 fail")
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,被关注用户的消息状态","fail")
            elif follow_msgStatus[0]['followCnt']==follow_msgStatus_init[0]['followCnt']+1:
                self.write_str(u"1.0.5-1.6 添加关注之后,被关注用户的消息状态 success")
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,被关注用户的消息状态","success")
            else:
                self.write_str(u"1.0.5-1.6 添加关注之后,被关注用户的消息状态 fail")
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,被关注用户的消息状态","fail")

            # # # 添加关注之后,影响被关注用户的消息列表 
            # ======================================== 6 =======================================
            msg_time1=self.get_now_time()
            ax ={}
            isMediaGetlist = self.ants_get_msg(0,2,4,persons[1],ax,pid)
            print(isMediaGetlist)
            msg_time2=self.get_now_time()
            if isMediaGetlist == -1 or isMediaGetlist == -100:
                self.write_str(u"1.0.5-1.6 添加关注之后,被关注用户的消息列表异常 error")
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,被关注用户的消息列表异常","error")
            elif isMediaGetlist == False:
                self.write_str(u"1.0.5-1.6 添加关注之后,影响被关注用户的消息列表 fail")
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,影响被关注用户的消息列表","fail")
            else:
                self.write_str(u"1.0.5-1.6 添加关注之后,影响被关注用户的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                self.write_email_log(u"1.0.5-1.6"," 添加关注之后,影响被关注用户的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")

            # # 取消关注 ====================================
            cel_follow_time1=self.get_now_time()
            isCancelFollow = self.ants_follow(pid,0,persons[1])
            cel_follow_time2=self.get_now_time()
            if isCancelFollow:
                self.write_str(u"1.0.5_2 取消关注 success，耗时"+str(self.get_time_long(cel_follow_time1,cel_follow_time2)))
                self.write_email_log(u"1.0.5_2"," 取消关注，耗时"+str(self.get_time_long(cel_follow_time1,cel_follow_time2)),"success")
            else:
                self.write_str(u"1.0.5_2 取消关注 fail")
                self.write_email_log(u"1.0.5_2"," 取消关注","fail")

            time.sleep(5)
            # # 取消关注之后,影响登录用户的关注列表 
            # ====================================== 1 =========================================
            followList_time3=self.get_now_time()
            isFollowListEnd = self.ants_fllowList(pid,1,persons[1])
            followList_time4=self.get_now_time()
            if isFollowListEnd== -1 or isFollowListEnd == -100:
                self.write_str(u"1.0.5-2.1 取消关注之后,登录用户的关注列表异常 error")
                self.write_email_log(u"1.0.5-2.1"," 取消关注之后,登录用户的关注列表异常","error")
            elif isFollowListEnd == False:
                self.write_str(u"1.0.5-2.1 取消关注之后,影响登录用户的关注列表 success，耗时"+str(self.get_time_long(followList_time3,followList_time4)))
                self.write_email_log(u"1.0.5-2.1"," 取消关注之后,影响登录用户的关注列表，耗时"+str(self.get_time_long(followList_time3,followList_time4)),"success")
            else:
                self.write_str(u"1.0.5-2.1 取消关注之后,影响登录用户的关注列表 fail")
                self.write_email_log(u"1.0.5-2.1"," 取消关注之后,影响登录用户的关注列表","fail")

            # # 取消关注之后,影响登录用户的个人信息  
            # ====================================== 2 =========================================
            userInfo_time5=self.get_now_time()
            result_follows_end = self.ants_get_user_info(persons[1],'follows',persons[1])
            print(result_follows_end)
            userInfo_time6=self.get_now_time()
            if result_follows==(result_follows_end+1):
                self.write_str(u"1.0.5-2.2 取消关注之后,影响登录用户的个人信息 success，耗时"+str(self.get_time_long(userInfo_time5,userInfo_time6)))
                self.write_email_log(u"1.0.5-2.2"," 取消关注之后,影响登录用户的个人信息，耗时"+str(self.get_time_long(userInfo_time5,userInfo_time6)),"success")
            else:
                self.write_str(u"1.0.5-2.2 取消关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-2.2"," 取消关注之后,影响登录用户的个人信息","fail")

            # # 取消关注之后,影响被关注用户的粉丝列表 
            # ======================================= 3 ========================================
            fanList_time3=self.get_now_time()
            isFollowFansEnd = self.ants_get_fanList_isIn(pid,-1,persons[1])
            fanList_time4=self.get_now_time()
            if not isFollowFansEnd:
                self.write_str(u"1.0.5-2.3 取消关注之后,影响被关注用户的粉丝列表 success，耗时"+str(self.get_time_long(fanList_time3,fanList_time4)))
                self.write_email_log(u"1.0.5-2.3 ","取消关注之后,影响被关注用户的粉丝列表，耗时"+str(self.get_time_long(fanList_time3,fanList_time4)),"success")
            else:
                self.write_str(u"1.0.5-2.3 取消关注之后,影响被关注用户的粉丝列表 fail")
                self.write_email_log(u"1.0.5-2.3 ","取消关注之后,影响被关注用户的粉丝列表","fail")
            
            
            # # 取消关注之后，影响被关注用户的个人信息 
            # ====================================== 4 =========================================
            userInfo_time7=self.get_now_time()
            result_login_info_fans_end = self.ants_get_user_info(pid,'fans',persons[1])
            userInfo_time8=self.get_now_time()
            print(result_login_info_fans_end)
            if result_login_info_fans==(result_login_info_fans_end+1):
                self.write_str(u"1.0.5-2.4 取消关注之后,影响被关注用户的个人信息 success，耗时"+str(self.get_time_long(userInfo_time7,userInfo_time8)))
                self.write_email_log(u"1.0.5-2.4 ","取消关注之后,影响被关注用户的个人信息，耗时"+str(self.get_time_long(userInfo_time7,userInfo_time8)),"success")
            else:
                self.write_str(u"1.0.5-2.4 取消关注之后,影响被关注用户的个人信息 fail")
                self.write_email_log(u"1.0.5-2.4 ","取消关注之后,影响被关注用户的个人信息","fail")
            
            # # 取消关注之后,影响登录用户查看被关注用户的媒体详情 
            # ====================================== 5 =========================================
            detail_time3=self.get_now_time()
            reult_share_media_detail_end = self.ants_media_detail(mediaId,persons[1])
            detail_time4=self.get_now_time()
            reult_share_media_detail_end_c = reult_share_media_detail_end[0]['isFollow']
            if reult_share_media_detail_end_c==0:
                self.write_str(u"1.0.5-2.5 取消关注之后,影响登录用户查看被关注用户的媒体详情 success，耗时"+str(self.get_time_long(detail_time3,detail_time4)))
                self.write_email_log(u"1.0.5-2.5 ","取消关注之后,影响登录用户查看被关注用户的媒体详情，耗时"+str(self.get_time_long(detail_time3,detail_time4)),"success")
            else:
                self.write_str(u"1.0.5-2.5 取消关注之后,影响登录用户查看被关注用户的媒体详情 fail")
                self.write_email_log(u"1.0.5-2.5 ","取消关注之后,影响登录用户查看被关注用户的媒体详情","fail")
           
            # # 取消关注之后,影响被关注用户的消息列表 
            # ====================================== 6 =========================================
            msg_time3=self.get_now_time()
            isMediaGetlistEnd = self.ants_get_msg(0,2,4,persons[1],{},pid)
            print(isMediaGetlistEnd)
            msg_time4=self.get_now_time()
            if isMediaGetlistEnd ==False:
                self.write_str(u"1.0.5-2.6 取消关注之后,影响被关注用户的消息列表 success，耗时"+str(self.get_time_long(msg_time3,msg_time4)))
                self.write_email_log(u"1.0.5-2.6 ","取消关注之后,影响被关注用户的消息列表"+str(self.get_time_long(msg_time3,msg_time4)),"success")
            else:
                self.write_str(u"1.0.5-2.6 取消关注之后,影响被关注用户的消息列表 fail")
                self.write_email_log(u"1.0.5-2.6 ","取消关注之后,影响被关注用户的消息列表","fail")

        # =============批量添加（取消）关注 =================================
        if RunCase:
            self.write_str("===========批量添加（取消）关注============")
            self.write_email_log('0000',"===========批量添加（取消）关注============","success")
            #先取消所有的已关注信息
            users=[pid,persons[2],persons[3],persons[4],persons[5]]
            result_fans={}
            result_msgStatus={}

            for x in range(len(users)):
                isFollowListEnd = self.ants_fllowList(users[x],1,persons[1])
                print(isFollowListEnd)
                if isFollowListEnd != False:
                    #取消关注
                    self.ants_follow(users[x],0,persons[1])
                    self.write_str('批量关注前，用户'+str(persons[1])+'取消关注用户'+str(users[x]))
                    self.write_email_log('1.0.5','批量关注前，用户'+str(persons[1])+'取消关注用户'+str(users[x]),'success')
                
                time.sleep(5)

                # # 添加关注之前,影响被关注用户的个人信息 
                # ============================================= 4 =================================
                result_login_info_fans_init_users = self.ants_get_user_info(users[x],'fans',persons[1])
                result_fans[users[x]]=result_login_info_fans_init_users
                print('用户'+str(users[x])+'初始fans值:'+str(result_login_info_fans_init_users))

                #添加关注之前，获取用户的消息状态
                follow_msgStatus_init_users_more = self.ants_get_msgStatus(users[x])
                result_msgStatus[users[x]]=follow_msgStatus_init_users_more
                print('用户'+str(users[x])+'初始消息状态:'+str(follow_msgStatus_init_users_more[0]['followCnt']))

            # # 添加关注之前,影响登录用户的个人信息  
            # ============================================= 2 =================================
            result_follows_more_init_users = self.ants_get_user_info(persons[1],'follows',persons[1])
            print('用户'+str(persons[1])+'初始follows值:'+str(result_follows_more_init_users))
            
            # # 添加关注 ==================================
            userIds=str(pid)+','+str(persons[2])+','+str(persons[3])+','+str(persons[4])+','+str(persons[5])

            add_time1=self.get_now_time()
            isAddFollow = self.ants_follow(userIds,1,persons[1])
            add_time2=self.get_now_time()
            print(isAddFollow)
            if isAddFollow == 'success':
                self.write_str(u"1.0.5_3 用户"+str(persons[1])+"批量添加关注"+str(userIds)+" success，耗时"+str(self.get_time_long(add_time1,add_time2)))
                self.write_email_log(u"1.0.5_3 ","用户"+str(persons[1])+"批量添加关注"+str(userIds)+"，耗时"+str(self.get_time_long(add_time1,add_time2)),"success")
            else:
                self.write_str(u"1.0.5_3 用户"+str(persons[1])+"批量添加关注"+str(userIds)+" fail")
                self.write_email_log(u"1.0.5_3 ","用户"+str(persons[1])+"批量添加关注"+str(userIds),"fail")

            time.sleep(5)

            # # 添加关注之后,影响登录用户的个人信息 
            # ========================================= 2 =====================================
            userInfo_time1=self.get_now_time()
            result_follows_more_users = self.ants_get_user_info(persons[1],'follows',persons[1])
            userInfo_time2=self.get_now_time()
            print('批量关注前用户follows：'+str(result_follows_more_init_users)+',批量关注后用户follows'+str(result_follows_more_users))
             
            if result_follows_more_users ==-1 or result_follows_more_users ==-100:
                self.write_str(u"1.0.5-3.1 添加关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-3.1 ","添加关注之后,影响登录用户的个人信息","fail")
            elif result_follows_more_users==(result_follows_more_init_users+5):
                self.write_str(u"1.0.5-3.1 添加关注之后,影响登录用户的个人信息follows success，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.5-3.1 ","添加关注之后,影响登录用户的个人信息follows，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.5-3.1 添加关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-3.1 ","添加关注之后,影响登录用户的个人信息","fail")
                self.write_email_log('0000','批量关注前用户follows：'+str(result_follows_more_init_users)+',批量关注后用户follows'+str(result_follows_more_users),'fail')


            for i in range(len(users)):
                # # 添加关注之后,影响登录用户的关注列表 
                # ========================================= 1 =====================================
                followList_time1=self.get_now_time()
                isFollowList_more = self.ants_fllowList(users[i],1,persons[1])
                followList_time2=self.get_now_time()
                print(isFollowList_more)
                if isFollowList_more ==-1 or isFollowList_more== -100:
                    self.write_str(u"1.0.5-3.2 用户"+str(persons[1])+"批量添加关注之后,关注列表异常 error")
                    self.write_email_log(u"1.0.5-3.2 ","用户"+str(persons[1])+"批量添加关注之后,关注列表异常","error")
                elif isFollowList_more == False:
                    self.write_str(u"1.0.5-3.2 用户"+str(persons[1])+"批量添加关注之后,关注列表无用户"+str(users[i])+" fail")
                    self.write_email_log(u"1.0.5-3.2 ","用户"+str(persons[1])+"批量添加关注之后,关注列表无用户"+str(users[i]),"fail")
                else:
                    self.write_str(u"1.0.5-3.2 用户"+str(persons[1])+"批量添加关注之后,关注列表有用户"+str(users[i])+" success，耗时"+str(self.get_time_long(followList_time1,followList_time2)))
                    self.write_email_log(u"1.0.5-3.2 ","用户"+str(persons[1])+"批量添加关注之后,关注列表有用户"+str(users[i])+"耗时"+str(self.get_time_long(followList_time1,followList_time2)),"success")

                # # 添加关注之后,影响被关注用户的粉丝列表 
                # ========================================= 3 =====================================
                fanList_time1=self.get_now_time()
                isFollowFans_more = self.ants_get_fanList_isIn(users[i],-1,persons[1])
                fanList_time2=self.get_now_time()
                print(isFollowFans_more)
                if isFollowFans_more ==-1 or isFollowFans_more==-100:
                    self.write_str(u"1.0.5-3.3 用户"+str(persons[1])+"批量添加关注之后,用户"+str(users[i])+"的粉丝列表异常 error")
                    self.write_email_log(u"1.0.5-3.3 ","用户"+str(persons[1])+"批量添加关注之后,用户"+str(users[i])+"的粉丝列表异常","error")
                elif isFollowFans_more != False:
                    self.write_str(u"1.0.5-3.3 用户"+str(persons[1])+"批量添加关注之后,用户"+str(users[i])+"的粉丝列表 success，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)))
                    self.write_email_log(u"1.0.5-3.3 ","用户"+str(persons[1])+"批量添加关注之后,用户"+str(users[i])+"的粉丝列表，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)),"success")
                else:
                    self.write_str(u"1.0.5-3.3 用户"+str(persons[1])+"批量添加关注之后,用户"+str(users[i])+"的粉丝列表 fail")
                    self.write_email_log(u"1.0.5-3.3 ","用户"+str(persons[1])+"批量添加关注之后,用户"+str(users[i])+"的粉丝列表","fail")
            
                # # 添加关注之后,影响被关注用户的个人信息 
                # ========================================= 4 =====================================
                userInfo_time3=self.get_now_time()
                result_login_info_fans = self.ants_get_user_info(users[i],'fans',persons[1])
                userInfo_time4=self.get_now_time()

                if result_login_info_fans==-1 or result_login_info_fans ==-100:
                    self.write_str(u"1.0.5-3.4 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-3.4 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的个人信息fans","fail")
                elif result_login_info_fans==(result_fans[users[i]]+1):
                    self.write_str(u"1.0.5-3.4 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                    self.write_email_log(u"1.0.5-3.4 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
                    print('批量关注前用户'+str(users[i])+'fans：'+str(result_fans[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans))
                else:
                    self.write_str(u"1.0.5-3.4 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-3.4 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的个人信息fans","fail")
                    self.write_str('批量关注前用户'+str(users[i])+'fans：'+str(result_fans[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans))
                    self.write_email_log('1.0.5-3.4','批量关注前用户'+str(users[i])+'fans：'+str(result_fans[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans),'fail')
            
                # 添加关注之后,影响被关注用户的消息状态 
                # ======================================== 6 =======================================
                follow_msgStatus_more = self.ants_get_msgStatus(users[i])
                print(follow_msgStatus_more)
                print("*******")
                follow_msgStatus_init_more = result_msgStatus[users[i]]

                if follow_msgStatus_more == -1 or follow_msgStatus_more == -100:
                    self.write_str(u"1.0.5-3.5 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态异常 error")
                    self.write_email_log(u"1.0.5-3.5 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态出现异常","error")
                elif follow_msgStatus_more == False:
                    self.write_str(u"1.0.5-3.5 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态 fail")
                    self.write_email_log(u"1.0.5-3.5 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态","fail")
                elif follow_msgStatus_more[0]['followCnt']==follow_msgStatus_init_more[0]['followCnt']+1:
                    self.write_str(u"1.0.5-3.5 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态 success")
                    self.write_email_log(u"1.0.5-3.5 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态","success")
                    self.write_str('批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more[0]['followCnt'])) 
                else:
                    self.write_str(u"1.0.5-3.5 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态 fail")
                    self.write_email_log(u"1.0.5-3.5 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息状态","fail")
                    self.write_str('1.0.5-3.5 批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more[0]['followCnt']))
                    self.write_email_log('1.0.5-3.5 ','批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more[0]['followCnt']),'fail')

                # 添加关注之后,影响被关注用户的消息列表 
                # ======================================== 6 =======================================
                msg_time1=self.get_now_time()
                ax ={}
                isMediaGetlist_more = self.ants_get_msg(0,2,4,persons[1],ax,users[i])
                print(isMediaGetlist_more)
                msg_time2=self.get_now_time()
                if isMediaGetlist_more == -1 or isMediaGetlist_more == -100:
                    self.write_str(u"1.0.5-3.6 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息列表异常 error")
                    self.write_email_log(u"1.0.5-3.6 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息列表异常","error")
                elif isMediaGetlist_more == False:
                    self.write_str(u"1.0.5-3.6 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息列表 fail")
                    self.write_email_log(u"1.0.5-3.6 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息列表","fail")
                else:
                    self.write_str(u"1.0.5-3.6 用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                    self.write_email_log(u"1.0.5-3.6 ","用户"+str(persons[1])+"批量添加关注之后,影响被关注用户"+str(users[i])+"的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")

            # # 添加关注之后,影响登录用户查看被关注用户的媒体详情 
            # ======================================== 5 ======================================
            detail_time1=self.get_now_time()
            media_detail_more = self.ants_media_detail(mediaId,persons[1])
            detail_time2=self.get_now_time()
            if media_detail_more ==-1 or media_detail_more==-100:
                self.write_str(u"1.0.5-3.7 用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                self.write_email_log(u"1.0.5-3.7 ","用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")
            else:
                media_detail_more_b = media_detail_more[0]['isFollow']
                if media_detail_more_b==1:
                    self.write_str(u"1.0.5-3.7 用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 success，耗时"+str(self.get_time_long(detail_time1,detail_time2)))
                    self.write_email_log(u"1.0.5-3.7 ","用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情，耗时"+str(self.get_time_long(detail_time1,detail_time2)),"success")
                else:
                    self.write_str(u"1.0.5-3.7 用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                    self.write_email_log(u"1.0.5-3.7 ","用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")


            # # 取消关注 ====================================
            cel_follow_time1=self.get_now_time()
            isCancelFollow_more = self.ants_follow(userIds,0,persons[1])
            cel_follow_time2=self.get_now_time()
            if isCancelFollow_more == 'success':
                self.write_str(u"1.0.5_4 用户"+str(persons[1])+"批量取消关注"+str(userIds)+" success，耗时"+str(self.get_time_long(cel_follow_time1,cel_follow_time2)))
                self.write_email_log(u"1.0.5_4 ","用户"+str(persons[1])+"批量取消关注"+str(userIds)+"，耗时"+str(self.get_time_long(cel_follow_time1,cel_follow_time2)),"success")
            else:
                self.write_str(u"1.0.5_4 用户"+str(persons[1])+"批量取消关注"+str(userIds)+" fail")
                self.write_email_log(u"1.0.5_4 ","用户"+str(persons[1])+"批量取消关注"+str(userIds),"fail")

            time.sleep(5)

            # # 取消关注之后,影响登录用户的个人信息 
            # ========================================= 2 =====================================
            userInfo_time1=self.get_now_time()
            result_follows_more_end_users = self.ants_get_user_info(persons[1],'follows',persons[1])
            userInfo_time2=self.get_now_time()
            print('批量取消关注前用户follows：'+str(result_follows_more_users)+',批量取消关注后用户follows'+str(result_follows_more_end_users))

            if result_follows_more_end_users ==-1 or result_follows_more_end_users ==-100:
                self.write_str(u"1.0.5-4.1 取消关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-4.1 ","取消关注之后,影响登录用户的个人信息","fail")
            elif result_follows_more_end_users==(result_follows_more_users-5):
                self.write_str(u"1.0.5-4.1 取消关注之后,影响登录用户的个人信息follows success，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.5-4.1 ","取消关注之后,影响登录用户的个人信息follows，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.5-4.1 取消关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-4.1 ","取消关注之后,影响登录用户的个人信息","fail")
                self.write_email_log('0000','批量取消关注前用户follows：'+str(result_follows_more_users)+',批量取消关注后用户follows'+str(result_follows_more_end_users),'fail')


            for y in range(len(users)):
                # 批量取消加关注之后,影响登录用户的关注列表 
                # ========================================= 1 =====================================
                followList_time1=self.get_now_time()
                isFollowList_end_more = self.ants_fllowList(users[y],1,persons[1])
                followList_time2=self.get_now_time()
                print(isFollowList_end_more)
                if isFollowList_end_more ==-1 or isFollowList_end_more== -100:
                    self.write_str(u"1.0.5-4.2 用户"+str(persons[1])+"批量取消关注之后,关注列表异常 error")
                    self.write_email_log(u"1.0.5-4.2 ","用户"+str(persons[1])+"批量取消关注之后,关注列表异常","error")
                elif isFollowList_end_more == False:
                    self.write_str(u"1.0.5-4.2 用户"+str(persons[1])+"批量取消关注之后,关注列表有用户"+str(users[y])+" success，耗时"+str(self.get_time_long(followList_time1,followList_time2)))
                    self.write_email_log(u"1.0.5-4.2 ","用户"+str(persons[1])+"批量取消关注之后,关注列表有用户"+str(users[y])+"耗时"+str(self.get_time_long(followList_time1,followList_time2)),"success")
                else:
                    self.write_str(u"1.0.5-4.2 用户"+str(persons[1])+"批量取消关注之后,关注列表无用户"+str(users[y])+" fail")
                    self.write_email_log(u"1.0.5-4.2 ","用户"+str(persons[1])+"批量取消关注之后,关注列表无用户"+str(users[y]),"fail")

                # 批量取消加关注之后,影响被关注用户的粉丝列表 
                # ========================================= 3 =====================================
                fanList_time1=self.get_now_time()
                isFollowFans_end_more = self.ants_get_fanList_isIn(users[y],-1,persons[1])
                fanList_time2=self.get_now_time()
                print(isFollowFans_end_more)
                if isFollowFans_end_more ==-1 or isFollowFans_end_more==-100:
                    self.write_str(u"1.0.5-4.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表异常 error")
                    self.write_email_log(u"1.0.5-4.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表异常","error")
                elif isFollowFans_end_more == False:
                    self.write_str(u"1.0.5-4.3 用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表 success，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)))
                    self.write_email_log(u"1.0.5-4.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)),"success")
                else:
                    self.write_str(u"1.0.5-4.3 用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表 fail")
                    self.write_email_log(u"1.0.5-4.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表","fail")
            
                # 批量取消加关注之后,影响被关注用户的个人信息 
                # ========================================= 4 =====================================
                userInfo_time3=self.get_now_time()
                result_login_info_fans_more_end = self.ants_get_user_info(users[y],'fans',persons[1])
                userInfo_time4=self.get_now_time()

                if result_login_info_fans_more_end==-1 or result_login_info_fans_more_end ==-100:
                    self.write_str(u"1.0.5-4.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-4.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans","fail")
                elif result_login_info_fans_more_end==result_fans[users[y]]:
                    self.write_str(u"1.0.5-4.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                    self.write_email_log(u"1.0.5-4.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
                    print('批量关注前用户'+str(users[y])+'fans：'+str(result_fans[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end))
                else:
                    self.write_str(u"1.0.5-4.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-4.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans","fail")
                    self.write_str('批量关注前用户'+str(users[y])+'fans：'+str(result_fans[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end))
                    self.write_email_log('0000','批量关注前用户'+str(users[y])+'fans：'+str(result_fans[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end),'fail')
            
                # 批量取消加关注之后,影响被关注用户的消息状态 
                # ======================================== 6 =======================================
                follow_msgStatus_more_end= self.ants_get_msgStatus(users[y])
                print(follow_msgStatus_more_end)
                print("*******")
                follow_msgStatus_init_more = result_msgStatus[users[y]]

                if follow_msgStatus_more_end == -1 or follow_msgStatus_more_end == -100:
                    self.write_str(u"1.0.5-4.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态异常 error")
                    self.write_email_log(u"1.0.5-4.5 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态出现异常","error")
                elif follow_msgStatus_more_end == False:
                    self.write_str(u"1.0.5-4.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态 fail")
                    self.write_email_log(u"1.0.5-4.5 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态","fail")
                elif follow_msgStatus_more_end[0]['followCnt']==follow_msgStatus_init_more[0]['followCnt']:
                    self.write_str(u"1.0.5-4.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态 success")
                    self.write_email_log(u"1.0.5-4.5 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态","success")
                    self.write_str('批量关注前用户'+str(users[y])+'msgStatus：'+str(follow_msgStatus_init_more[0]['followCnt'])+',批量取消关注后用户msgStatus：'+str(follow_msgStatus_more_end[0]['followCnt'])) 
                else:
                    self.write_str(u"1.0.5-4.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态 fail")
                    self.write_email_log(u"1.0.5-4.5 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态","fail")
                    self.write_str('1.0.5-4.5 ','批量关注前用户'+str(users[y])+'msgStatus：'+str(follow_msgStatus_init_more[0]['followCnt'])+',批量取消关注后用户msgStatus：'+str(follow_msgStatus_more_end[0]['followCnt']))
                    self.write_email_log('1.0.5-4.5 批量关注前用户'+str(users[y])+'msgStatus：'+str(follow_msgStatus_init_more[0]['followCnt'])+',批量取消关注后用户msgStatus：'+str(follow_msgStatus_more_end[0]['followCnt']),'fail')

                #批量取消加关注之后,影响被关注用户的消息列表 
                # ======================================== 6 =======================================
                msg_time1=self.get_now_time()
                ax ={}
                isMediaGetlist_more_end = self.ants_get_msg(0,2,4,persons[1],ax,users[y])
                print(isMediaGetlist_more_end)
                msg_time2=self.get_now_time()
                if isMediaGetlist_more_end == -1 or isMediaGetlist_more_end == -100:
                    self.write_str(u"1.0.5-4.6 用户"+str(persons[1])+"批量取消加关注之后,影响被关注用户"+str(users[y])+"的消息列表异常 error")
                    self.write_email_log(u"1.0.5-4.6 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表异常","error")
                elif isMediaGetlist_more_end == False:
                    self.write_str(u"1.0.5-4.6 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                    self.write_email_log(u"1.0.5-4.6 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")
                else:
                    self.write_str(u"1.0.5-4.6 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表 fail")
                    self.write_email_log(u"1.0.5-4.6 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表","fail")

            # 批量取消加关注之后,影响登录用户查看被关注用户的媒体详情 
            # ======================================== 5 ======================================
            detail_time1=self.get_now_time()
            media_detail_more_end = self.ants_media_detail(mediaId,persons[1])
            detail_time2=self.get_now_time()
            if media_detail_more_end ==-1 or media_detail_more_end==-100:
                self.write_str(u"1.0.5-4.7 用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                self.write_email_log(u"1.0.5-4.7 ","用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")
            else:
                media_detail_more_end_b = media_detail_more_end[0]['isFollow']
                if media_detail_more_end_b==0:
                    self.write_str(u"1.0.5-4.7 用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 success，耗时"+str(self.get_time_long(detail_time1,detail_time2)))
                    self.write_email_log(u"1.0.5-4.7 ","用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情，耗时"+str(self.get_time_long(detail_time1,detail_time2)),"success")
                else:
                    self.write_str(u"1.0.5-4.7 用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                    self.write_email_log(u"1.0.5-4.7 ","用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")
           
        # =============批量添加（取消）关注 =================================
        if RunCase:
            self.write_str("===========批量添加（取消）关注,内含一个已经关注的用户============")
            self.write_email_log('0000',"===========批量添加（取消）关注，内含一个已经关注的用户============","success")
            #先取消除pid之外的所有的已关注信息
            users=[pid,persons[2],persons[3],persons[4],persons[5]]
            result_fans2={}
            result_msgStatus2={}

            for x in range(len(users)):
                isFollowListEnd2 = self.ants_fllowList(users[x],1,persons[1])
                print(isFollowListEnd2)
                if users[x] ==pid and isFollowListEnd2 == False:
                    #如果person[0]，添加关注
                    addFollow = self.ants_follow(users[x],1,persons[1])
                    print(addFollow)
                    if addFollow=="success":
                        self.write_str('1.0.5 批量关注前，用户'+str(persons[1])+'添加关注用户'+str(users[x])+'success')
                        self.write_email_log('1.0.5','批量关注前，用户'+str(persons[1])+'添加关注用户'+str(users[x]),'success')
                    else:
                        self.write_str('1.0.5 批量关注前，用户'+str(persons[1])+'添加关注用户'+str(users[x])+'fail')
                        self.write_email_log('1.0.5','批量关注前，用户'+str(persons[1])+'添加关注用户'+str(users[x]),'fail')
                    
                elif users[x] != pid and isFollowListEnd2 != False:
                    #取消关注
                    self.ants_follow(users[x],0,persons[1])
                    self.write_str('1.0.5 批量关注前，用户'+str(persons[1])+'取消关注用户'+str(users[x]))
                    self.write_email_log('1.0.5','批量关注前，用户'+str(persons[1])+'取消关注用户'+str(users[x]),'success')
                
                time.sleep(5)

                # # 添加关注之前,影响被关注用户的个人信息 
                # ============================================= 4 =================================
                result_login_info_fans_init_users2 = self.ants_get_user_info(users[x],'fans',persons[1])
                result_fans2[users[x]]=result_login_info_fans_init_users2
                print('用户'+str(users[x])+'初始fans值:'+str(result_login_info_fans_init_users2))

                #添加关注之前，获取用户的消息状态
                follow_msgStatus_init_users_more2 = self.ants_get_msgStatus(users[x])
                result_msgStatus2[users[x]]=follow_msgStatus_init_users_more2
                print('用户'+str(users[x])+'初始消息状态:'+str(follow_msgStatus_init_users_more2[0]['followCnt']))

            

            # # 添加关注之前,影响登录用户的个人信息  
            # ============================================= 2 =================================
            result_follows_more_init_users2 = self.ants_get_user_info(persons[1],'follows',persons[1])
            print('用户'+str(persons[1])+'初始follows值:'+str(result_follows_more_init_users2))
            
            # # 添加关注 ==================================
            userIds=str(pid)+','+str(persons[2])+','+str(persons[3])+','+str(persons[4])+','+str(persons[5])

            add_time1=self.get_now_time()
            isAddFollow2 = self.ants_follow(userIds,1,persons[1])
            add_time2=self.get_now_time()
            print(isAddFollow2)
            if isAddFollow2 == 'success':
                self.write_str(u"1.0.5_5 用户"+str(persons[1])+"批量添加关注"+str(userIds)+"("+str(pid)+"已关注) success，耗时"+str(self.get_time_long(add_time1,add_time2)))
                self.write_email_log(u"1.0.5_5 ","用户"+str(persons[1])+"批量添加关注"+str(userIds)+"("+str(pid)+"已关注)，耗时"+str(self.get_time_long(add_time1,add_time2)),"success")
            else:
                self.write_str(u"1.0.5_5 用户"+str(persons[1])+"批量添加关注"+str(userIds)+"("+str(pid)+"已关注) fail")
                self.write_email_log(u"1.0.5_5 ","用户"+str(persons[1])+"批量添加关注"+str(userIds)+"("+str(pid)+"已关注)","fail")

            time.sleep(5)

            # # 添加关注之后,影响登录用户的个人信息 
            # ========================================= 2 =====================================
            userInfo_time1=self.get_now_time()
            result_follows_more_users2 = self.ants_get_user_info(persons[1],'follows',persons[1])
            userInfo_time2=self.get_now_time()
            print('批量关注前用户follows：'+str(result_follows_more_init_users2)+",批量关注("+str(pid)+"已关注)后用户follows"+str(result_follows_more_users2))
             
            if result_follows_more_users2 ==-1 or result_follows_more_users2 ==-100:
                self.write_str(u"1.0.5-5.1 添加关注("+str(pid)+"已关注)之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-5.1 ","添加关注("+str(pid)+"已关注)之后,影响登录用户的个人信息","fail")
            elif result_follows_more_users2==(result_follows_more_init_users2+4):
                self.write_str(u"1.0.5-5.1 添加关注("+str(pid)+"已关注)之后,影响登录用户的个人信息follows success，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.5-5.1 ","添加关注("+str(pid)+"已关注)之后,影响登录用户的个人信息follows，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.5-5.1 添加关注("+str(pid)+"已关注)之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-5.1 ","添加关注("+str(pid)+"已关注)之后,影响登录用户的个人信息","fail")
                self.write_email_log('1.0.5-5.1',"批量关注("+str(pid)+"已关注)前用户follows："+str(result_follows_more_init_users2)+",批量关注后用户follows"+str(result_follows_more_users2),'fail')


            for i in range(len(users)):
                # # 添加关注之后,影响登录用户的关注列表 
                # ========================================= 1 =====================================
                followList_time1=self.get_now_time()
                isFollowList_more2 = self.ants_fllowList(users[i],1,persons[1])
                followList_time2=self.get_now_time()
                print(isFollowList_more2)
                if isFollowList_more2 ==-1 or isFollowList_more2 == -100:
                    self.write_str(u"1.0.5-5.2 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,关注列表异常 error")
                    self.write_email_log(u"1.0.5-5.2 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,关注列表异常","error")
                elif isFollowList_more2 == False:
                    self.write_str(u"1.0.5-5.2 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,关注列表无用户"+str(users[i])+" fail")
                    self.write_email_log(u"1.0.5-5.2 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,关注列表无用户"+str(users[i]),"fail")
                else:
                    self.write_str(u"1.0.5-5.2 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,关注列表有用户"+str(users[i])+" success，耗时"+str(self.get_time_long(followList_time1,followList_time2)))
                    self.write_email_log(u"1.0.5-5.2 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,关注列表有用户"+str(users[i])+"耗时"+str(self.get_time_long(followList_time1,followList_time2)),"success")

                # # 添加关注之后,影响被关注用户的粉丝列表 
                # ========================================= 3 =====================================
                fanList_time1=self.get_now_time()
                isFollowFans_more2 = self.ants_get_fanList_isIn(users[i],-1,persons[1])
                fanList_time2=self.get_now_time()
                print(isFollowFans_more2)
                if isFollowFans_more2 ==-1 or isFollowFans_more2 ==-100:
                    self.write_str(u"1.0.5-5.3 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,用户"+str(users[i])+"的粉丝列表异常 error")
                    self.write_email_log(u"1.0.5-5.3 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,用户"+str(users[i])+"的粉丝列表异常","error")
                elif isFollowFans_more2 != False:
                    self.write_str(u"1.0.5-5.3 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,用户"+str(users[i])+"的粉丝列表 success，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)))
                    self.write_email_log(u"1.0.5-5.3 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,用户"+str(users[i])+"的粉丝列表，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)),"success")
                else:
                    self.write_str(u"1.0.5-5.3 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,用户"+str(users[i])+"的粉丝列表 fail")
                    self.write_email_log(u"1.0.5-5.3 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,用户"+str(users[i])+"的粉丝列表","fail")
            
                # # 添加关注之后,影响被关注用户的个人信息 
                # ========================================= 4 =====================================
                userInfo_time3=self.get_now_time()
                result_login_info_fans2 = self.ants_get_user_info(users[i],'fans',persons[1])
                userInfo_time4=self.get_now_time()

                if result_login_info_fans2==-1 or result_login_info_fans2 ==-100:
                    self.write_str(u"1.0.5-5.4 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-5.4 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的个人信息fans","fail")
                elif users[i] == pid and result_login_info_fans2 == result_fans2[users[i]]:
                    self.write_str(u"1.0.5-5.4 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,不影响被关注用户"+str(users[i])+"的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                    self.write_email_log(u"1.0.5-5.4 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,不影响被关注用户"+str(users[i])+"的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
                    print('批量关注前用户'+str(users[i])+'fans：'+str(result_fans2[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans2))
                elif users[i] != pid and result_login_info_fans2 == (result_fans2[users[i]]+1):
                    self.write_str(u"1.0.5-5.4 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                    self.write_email_log(u"1.0.5-5.4 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
                    print('批量关注前用户'+str(users[i])+'fans：'+str(result_fans2[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans2))
                else:
                    self.write_str(u"1.0.5-5.4 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-5.4 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的个人信息fans","fail")
                    self.write_str('批量关注前用户'+str(users[i])+'fans：'+str(result_fans2[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans2))
                    self.write_email_log('1.0.5-5.4','批量关注前用户'+str(users[i])+'fans：'+str(result_fans2[users[i]])+',批量关注后用户fans：'+str(result_login_info_fans2),'fail')
            
                # 添加关注之后,影响被关注用户的消息状态 
                # ======================================== 6 =======================================
                follow_msgStatus_more2 = self.ants_get_msgStatus(users[i])
                print(follow_msgStatus_more2)
                print("*******")
                follow_msgStatus_init_more2 = result_msgStatus2[users[i]]

                if follow_msgStatus_more2 == -1 or follow_msgStatus_more2 == -100:
                    self.write_str(u"1.0.5-5.5 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态异常 error")
                    self.write_email_log(u"1.0.5-5.5 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态出现异常","error")
                elif follow_msgStatus_more2 == False:
                    self.write_str(u"1.0.5-5.5 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态 fail")
                    self.write_email_log(u"1.0.5-5.5 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态","fail")
                elif users[i] != pid and follow_msgStatus_more2[0]['followCnt']==follow_msgStatus_init_more2[0]['followCnt']+1:
                    self.write_str(u"1.0.5-5.5 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态 success")
                    self.write_email_log(u"1.0.5-5.5 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态","success")
                    self.write_str('批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more2[0]['followCnt'])) 
                elif users[i] == pid and follow_msgStatus_more2[0]['followCnt']==follow_msgStatus_init_more2[0]['followCnt']:
                    self.write_str(u"1.0.5-5.5 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态 success")
                    self.write_email_log(u"1.0.5-5.5 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态","success")
                    self.write_str('批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more2[0]['followCnt'])) 
                else:
                    self.write_str(u"1.0.5-5.5 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态 fail")
                    self.write_email_log(u"1.0.5-5.5 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息状态","fail")
                    self.write_str('1.0.5-5.5 批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more2[0]['followCnt']))
                    self.write_email_log('1.0.5-5.5 ","批量关注前用户'+str(users[i])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量关注后用户msgStatus：'+str(follow_msgStatus_more2[0]['followCnt']),'fail')

                # 添加关注之后,影响被关注用户的消息列表 
                # ======================================== 6 =======================================
                msg_time1=self.get_now_time()
                ax ={}
                isMediaGetlist_more2 = self.ants_get_msg(0,2,4,persons[1],ax,users[i])
                print(isMediaGetlist_more2)
                msg_time2=self.get_now_time()
                if isMediaGetlist_more2 == -1 or isMediaGetlist_more2 == -100:
                    self.write_str(u"1.0.5-5.6 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息列表异常 error")
                    self.write_email_log(u"1.0.5-5.6 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息列表异常","error")
                elif isMediaGetlist_more2 != False:
                    self.write_str(u"1.0.5-5.6 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                    self.write_email_log(u"1.0.5-5.6 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")
                else:
                    self.write_str(u"1.0.5-5.6 用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息列表 fail")
                    self.write_email_log(u"1.0.5-5.6 ","用户"+str(persons[1])+"批量添加关注("+str(pid)+"已关注)之后,影响被关注用户"+str(users[i])+"的消息列表","fail")

            # # 添加关注之后,影响登录用户查看被关注用户的媒体详情 
            # ======================================== 5 ======================================
            detail_time1=self.get_now_time()
            media_detail_more2 = self.ants_media_detail(mediaId,persons[1])
            detail_time2=self.get_now_time()
            if media_detail_more2 ==-1 or media_detail_more2==-100:
                self.write_str(u"1.0.5-5.7 用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                self.write_email_log(u"1.0.5-5.7 ","用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")
            else:
                media_detail_more_b2 = media_detail_more2[0]['isFollow']
                if media_detail_more_b2==1:
                    self.write_str(u"1.0.5-5.7 用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 success，耗时"+str(self.get_time_long(detail_time1,detail_time2)))
                    self.write_email_log(u"1.0.5-5.7 ","用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情，耗时"+str(self.get_time_long(detail_time1,detail_time2)),"success")
                else:
                    self.write_str(u"1.0.5-5.7 用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                    self.write_email_log(u"1.0.5-5.7 ","用户"+str(persons[1])+"批量添加关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")


            # # 取消关注 ====================================
            cel_follow_time1=self.get_now_time()
            isCancelFollow_more2 = self.ants_follow(userIds,0,persons[1])
            cel_follow_time2=self.get_now_time()
            if isCancelFollow_more2 == 'success':
                self.write_str(u"1.0.5_6 用户"+str(persons[1])+"批量取消关注"+str(userIds)+" success，耗时"+str(self.get_time_long(cel_follow_time1,cel_follow_time2)))
                self.write_email_log(u"1.0.5_6 ","用户"+str(persons[1])+"批量取消关注"+str(userIds)+"，耗时"+str(self.get_time_long(cel_follow_time1,cel_follow_time2)),"success")
            else:
                self.write_str(u"1.0.5_6 用户"+str(persons[1])+"批量取消关注"+str(userIds)+" fail")
                self.write_email_log(u"1.0.5_6 ","用户"+str(persons[1])+"批量取消关注"+str(userIds),"fail")

            time.sleep(5)
            
            # # 取消关注之后,影响登录用户的个人信息 
            # ========================================= 2 =====================================
            userInfo_time1=self.get_now_time()
            result_follows_more_end_users2 = self.ants_get_user_info(persons[1],'follows',persons[1])
            userInfo_time2=self.get_now_time()
            print('批量取消关注前用户follows：'+str(result_follows_more_users2)+',批量取消关注后用户follows'+str(result_follows_more_end_users2))
             
            if result_follows_more_end_users2 ==-1 or result_follows_more_end_users2 ==-100:
                self.write_str(u"1.0.5-6.1 取消关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-6.1 ","取消关注之后,影响登录用户的个人信息","fail")
            elif result_follows_more_end_users2==(result_follows_more_users2-5):
                self.write_str(u"1.0.5-6.1 取消关注之后,影响登录用户的个人信息follows success，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.5-6.1 ","取消关注之后,影响登录用户的个人信息follows，耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.5-6.1 取消关注之后,影响登录用户的个人信息 fail")
                self.write_email_log(u"1.0.5-6.1 ","取消关注之后,影响登录用户的个人信息","fail")
                self.write_email_log('0000','批量取消关注前用户follows：'+str(result_follows_more_users2)+',批量取消关注后用户follows'+str(result_follows_more_end_users2),'fail')


            for y in range(len(users)):
                # 批量取消加关注之后,影响登录用户的关注列表 
                # ========================================= 1 =====================================
                followList_time1=self.get_now_time()
                isFollowList_end_more2 = self.ants_fllowList(users[y],1,persons[1])
                followList_time2=self.get_now_time()
                print(isFollowList_end_more2)
                if isFollowList_end_more2 ==-1 or isFollowList_end_more2== -100:
                    self.write_str(u"1.0.5-6.2 用户"+str(persons[1])+"批量取消关注之后,关注列表异常 error")
                    self.write_email_log(u"1.0.5-6.2 ","用户"+str(persons[1])+"批量取消关注之后,关注列表异常","error")
                elif isFollowList_end_more2 == False:
                    self.write_str(u"1.0.5-6.2 用户"+str(persons[1])+"批量取消关注之后,关注列表有用户"+str(users[y])+" success，耗时"+str(self.get_time_long(followList_time1,followList_time2)))
                    self.write_email_log(u"1.0.5-6.2 ","用户"+str(persons[1])+"批量取消关注之后,关注列表有用户"+str(users[y])+"耗时"+str(self.get_time_long(followList_time1,followList_time2)),"success")
                else:
                    self.write_str(u"1.0.5-6.2 用户"+str(persons[1])+"批量取消关注之后,关注列表无用户"+str(users[y])+" fail")
                    self.write_email_log(u"1.0.5-6.2 ","用户"+str(persons[1])+"批量取消关注之后,关注列表无用户"+str(users[y]),"fail")

                # 批量取消加关注之后,影响被关注用户的粉丝列表 
                # ========================================= 3 =====================================
                fanList_time1=self.get_now_time()
                isFollowFans_end_more2 = self.ants_get_fanList_isIn(users[y],-1,persons[1])
                fanList_time2=self.get_now_time()
                print(isFollowFans_end_more2)
                if isFollowFans_end_more2 ==-1 or isFollowFans_end_more2==-100:
                    self.write_str(u"1.0.5-6.3 用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表异常 error")
                    self.write_email_log(u"1.0.5-6.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表异常","error")
                elif isFollowFans_end_more2 == False:
                    self.write_str(u"1.0.5-6.3 用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表 success，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)))
                    self.write_email_log(u"1.0.5-6.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表，耗时"+str(self.get_time_long(fanList_time1,fanList_time2)),"success")
                else:
                    self.write_str(u"1.0.5-6.3 用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表 fail")
                    self.write_email_log(u"1.0.5-6.3 ","用户"+str(persons[1])+"批量取消关注之后,用户"+str(users[y])+"的粉丝列表","fail")
            
                # # 批量取消加关注之后,影响被关注用户的个人信息 
                # ========================================= 4 =====================================
                userInfo_time3=self.get_now_time()
                result_login_info_fans_more_end2 = self.ants_get_user_info(users[y],'fans',persons[1])
                userInfo_time4=self.get_now_time()

                if result_login_info_fans_more_end2==-1 or result_login_info_fans_more_end2 ==-100:
                    self.write_str(u"1.0.5-6.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-6.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans","fail")
                elif users[y] != pid and result_login_info_fans_more_end2==result_fans2[users[y]]:
                    self.write_str(u"1.0.5-6.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                    self.write_email_log(u"1.0.5-6.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
                    print('批量关注前用户'+str(users[y])+'fans：'+str(result_fans2[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end2))
                elif users[y] == pid and result_login_info_fans_more_end2==result_fans2[users[y]]-1:
                    self.write_str(u"1.0.5-6.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans success，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)))
                    self.write_email_log(u"1.0.5-6.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans，耗时"+str(self.get_time_long(userInfo_time3,userInfo_time4)),"success")
                    print('批量关注前用户'+str(users[y])+'fans：'+str(result_fans2[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end2))
                else:
                    self.write_str(u"1.0.5-6.4 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans fail")
                    self.write_email_log(u"1.0.5-6.4 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的个人信息fans","fail")
                    self.write_str('批量关注前用户'+str(users[y])+'fans：'+str(result_fans2[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end2))
                    self.write_email_log('1.0.5-6.4','批量关注前用户'+str(users[y])+'fans：'+str(result_fans2[users[y]])+',批量取消关注后用户fans：'+str(result_login_info_fans_more_end2),'fail')
            
                # # 批量取消加关注之后,影响被关注用户的消息状态 
                # # ======================================== 6 =======================================
                # follow_msgStatus_more_end2= self.ants_get_msgStatus(users[y])
                # print(follow_msgStatus_more_end2)
                # print("*******")
                # follow_msgStatus_init_more2 = result_msgStatus2[users[y]]

                # if follow_msgStatus_more_end2 == -1 or follow_msgStatus_more_end2 == -100:
                #     self.write_str(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态异常 error")
                #     self.write_email_log(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态出现异常","error")
                # elif follow_msgStatus_more_end2 == False:
                #     self.write_str(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态 fail")
                #     self.write_email_log(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态","fail")
                # elif follow_msgStatus_more_end2[0]['followCnt']==follow_msgStatus_init_more2[0]['followCnt']:
                #     self.write_str(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态 success")
                #     self.write_email_log(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态","success")
                #     self.write_str('批量关注前用户'+str(users[y])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量取消关注后用户msgStatus：'+str(follow_msgStatus_more_end2[0]['followCnt'])) 
                # else:
                #     self.write_str(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态 fail")
                #     self.write_email_log(u"1.0.5-6.5 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息状态","fail")
                #     self.write_str('1.0.5-6.5 批量关注前用户'+str(users[y])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量取消关注后用户msgStatus：'+str(follow_msgStatus_more_end2[0]['followCnt']))
                #     self.write_email_log('1.0.5-6.5 批量关注前用户'+str(users[y])+'msgStatus：'+str(follow_msgStatus_init_more2[0]['followCnt'])+',批量取消关注后用户msgStatus：'+str(follow_msgStatus_more_end2[0]['followCnt']),'fail')

                # 批量取消加关注之后,影响被关注用户的消息列表 
                # ======================================== 6 =======================================
                msg_time1=self.get_now_time()
                ax ={}
                isMediaGetlist_more_end2 = self.ants_get_msg(0,2,4,persons[1],ax,users[y])
                print(isMediaGetlist_more_end2)
                msg_time2=self.get_now_time()
                if isMediaGetlist_more_end2 == -1 or isMediaGetlist_more_end2 == -100:
                    self.write_str(u"1.0.5-6.6 用户"+str(persons[1])+"批量取消加关注之后,影响被关注用户"+str(users[y])+"的消息列表异常 error")
                    self.write_email_log(u"1.0.5-6.6 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表异常","error")
                elif isMediaGetlist_more_end2 == False:
                    self.write_str(u"1.0.5-6.6 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                    self.write_email_log(u"1.0.5-6.6 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")
                else:
                    self.write_str(u"1.0.5-6.6 用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表 fail")
                    self.write_email_log(u"1.0.5-6.6 ","用户"+str(persons[1])+"批量取消关注之后,影响被关注用户"+str(users[y])+"的消息列表","fail")

            # 批量取消加关注之后,影响登录用户查看被关注用户的媒体详情 
            # ======================================== 5 ======================================
            detail_time1=self.get_now_time()
            media_detail_more_end2 = self.ants_media_detail(mediaId,persons[1])
            detail_time2=self.get_now_time()
            if media_detail_more_end2 ==-1 or media_detail_more_end2==-100:
                self.write_str(u"1.0.5-6.7 用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                self.write_email_log(u"1.0.5-6.7 ","用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")
            else:
                media_detail_more_end_b2 = media_detail_more_end2[0]['isFollow']
                if media_detail_more_end_b2==0:
                    self.write_str(u"1.0.5-6.7 用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 success，耗时"+str(self.get_time_long(detail_time1,detail_time2)))
                    self.write_email_log(u"1.0.5-6.7 ","用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情，耗时"+str(self.get_time_long(detail_time1,detail_time2)),"success")
                else:
                    self.write_str(u"1.0.5-6.7 用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情 fail")
                    self.write_email_log(u"1.0.5-6.7 ","用户"+str(persons[1])+"批量取消关注之后,影响"+str(persons[1])+"查看"+str(pid)+"的媒体详情","fail")

        # 结束测试
        self.close_fd()
        self.EndTest()

        

def main():
    reload(sys)

    
    server,persons,serve_yy,server_firmware= inifile.get_input_params()
    cases = Follow(server,serve_yy,"five")
    cases.run_follow(persons)


if __name__=="__main__":
    main()