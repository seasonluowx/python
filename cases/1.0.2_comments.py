# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/2/15
# ----------------------

import os
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# print(crupath
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)
import time

# False


class Comment(Common):


    def __init__(self,server,serve_yy,ModuleName):
        Common.__init__(self,server,serve_yy,ModuleName)


    def run_case(self,persons):
        # print("run comment case"
        isFalse = False
        isRunlike = False
        isRunClub =False
        isRunTag = False
        mediaId = self.get_mediaId()
        print('mediaId:'+str(mediaId))
        mediaId = int(mediaId)
        if mediaId != 0:
            isFalse = True
            pass

        userId=self.get_pid()
        pid=int(userId)
       
        if isFalse:
            # 添加评论之前,媒体详情  
            # ============================== 1 ==========================================
            comments_init = self.ants_media_detail(mediaId,persons[1])
            print(comments_init)
            if comments_init ==-1 or comments_init==-100:
                self.write_str('1.0.2 媒体详情访问异常')
                self.write_email_log('1.0.2','媒体详情访问异常','fail')
            else:
                cn_init = comments_init[0]['comments']
                cmList_init = comments_init[0]['commentResList']
                print('cmList_init:'+str(cmList_init))

                #获取tag信息
                tags = comments_init[0]['tags']
                if tags != '':
                    tagIds=tags.split(",")
                    tagId=tagIds[0]
                    isRunTag =True
                    print('tagId:'+str(tagId))
                #获取club信息   
                tagList_init = comments_init[0]['tagList']
                for x in range(len(tagList_init)):
                    if tagList_init[x]['mediaSpecial'] == 10:
                        clubId=tagList_init[x]['id']
                        isRunClub =True
                        print('clubId:'+str(clubId))

            # self.write_str('============')
            # self.write_str(str(clubId))
            # self.write_str(str(len(cmList_init)))
        
            # # 添加评论之前,影响评论列表 
            # ============================== 2 ======================================
            cn_numbers_init = self.ants_get_comments_list(mediaId,persons[1])

            # 添加评论之前,影响媒体发布人的分享列表 
            # =============================== 5 =====================================
            comments_count_init = self.ants_private_share(pid,'mediaId',mediaId,'comments',persons[1])

        
            # 添加评论之前,影响标签最新列表 
            # =============================== 6 =====================================
            if isRunTag:
                tag_least_comments_init = self.ants_tags_least(tagId,'mediaId',mediaId,'comments',persons[1])
                tag_least_commentResList_init = self.ants_tags_least(tagId,'mediaId',mediaId,'commentResList',persons[1])
                print(str(tag_least_comments_init)+'***'+str(len(tag_least_commentResList_init)))
        
            # # 添加评论之前,影响首页列表 
            # =============================== 7 =====================================
            index_comments_init = self.ants_index('mediaId',mediaId,'comments',pid)
            index_commentResList_init = self.ants_index('mediaId',mediaId,'commentResList',pid)
            # print(str(index_comments_init)+'+888'+str(len(index_commentResList_init))
        
            # # 添加评论之前,影响俱乐部最新列表 
            # =============================== 8 =====================================
            if isRunClub:
                comments_club_init = self.ants_club_latest(clubId,'mediaId',mediaId,'comments',pid)
                commentResList_club_init = self.ants_club_latest(clubId,'mediaId',mediaId,'commentResList',pid)

            # 添加评论之前,影响点赞过的用户的喜欢列表 
            # =============================== 9 =============== 需要先点赞 ==========
            # 点赞
            bodys = {}
            bodys['mediaId'] = mediaId
            bodys['doLike'] = True
            status=self.ants_like(mediaId,bodys,persons[2])
            if  status == 'success':
                self.write_str(u"点赞 success")

                time.sleep(5)

                comments_count_like_init = self.ants_likeList(persons[2],'mediaId',mediaId,'comments',persons[1])
                #print(comments_count_like_init
                isRunlike = True
                pass
            
            #===通知状态===================================
            add_msgStatus_init_pid = self.ants_get_msgStatus(pid)
            print(add_msgStatus_init_pid)

            add_msgStatus_init_uid = self.ants_get_msgStatus(persons[2])
            print(add_msgStatus_init_uid)

        if isFalse:       
            # ==================== 添加评论 =================================================================
            add_time1= self.get_now_time();
            bodys = {}
            bodys['content'] = self.get_random() + ' === Good !===> '+ self.get_local_time()
            bodys['mediaId'] = mediaId
            bodys['userId'] = persons[2]
            add_result = self.ants_add_comment(mediaId,bodys,persons[1])
            add_time2 =self.get_now_time();
            if add_result == 'success':
                self.write_str(u"1.0.2-1 添加评论成功！耗时"+str(self.get_time_long(add_time1,add_time2)))
                self.write_email_log('1.0.2-1',"添加评论成功！耗时"+str(self.get_time_long(add_time1,add_time2)),'success')
            else:
                self.write_str(u"1.0.2-1 添加评论 fail")
                self.write_email_log('1.0.2-1',"加评论","fail")
            
            time.sleep(5)
        if isFalse:
            # 添加评论之后,媒体详情 =================================== 1 ======================================
            comment_time1= self.get_now_time()
            comments = self.ants_media_detail(mediaId,persons[1])
            if comments ==-1 or comments == -100:
                self.write_str("1.0.2-1.1 添加评论后，媒体详情出现异常 error")
                self.write_email_log('1.0.2-1.1',"添加评论后，媒体详情出现异","error")
            else:
                cn = comments[0]['comments']
                cmList = comments[0]['commentResList']
                print('cmList:'+str(cmList))
                # self.write_str(str(cn))
                # self.write_str(str(cmList))
                # self.write_str(str(cmList_init))
                # self.write_str('===========')
                comment_time2= self.get_now_time()
                # 得到最新评价的commentId
                commemt_id = self.get_new_commentId(cmList_init,cmList)
                print(commemt_id)
                
                if commemt_id == 0:
                    self.write_str(u"1.0.2-1.1 添加评论影响媒体详情fail")
                    self.write_email_log('1.0.2-1.1',"添加评论影响媒体详情","fail")
                elif commemt_id['commentId'] != 0 and cn==(cn_init+1):
                    self.write_str(u"1.0.2-1.1 添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id['commentId'])+",comments:"+str(cn)+',耗时'+str(self.get_time_long(comment_time1,comment_time2)))
                    self.write_email_log('1.0.2-1.1',"添加评论影响媒体详情成功！得到最新评价的commentId " + str(commemt_id['commentId'])+',耗时'+str(self.get_time_long(comment_time1,comment_time2)),"success")
                else:
                    self.write_str(u"1.0.2-1.1 添加影响媒体详情fail")
                    self.write_email_log('1.0.2-1.1',"添加评论影响媒体详情","fail")

                time.sleep(5)
                
                # # 添加评论之后,影响评论列表 
                # ================================= 2 ============================================
                cn_numbers_time1 = self.get_now_time()
                cn_numbers = self.ants_get_comments_list(mediaId,persons[1])
                commemt_id_new = self.get_new_commentId(cn_numbers_init,cn_numbers)
                cn_numbers_time2 =self.get_now_time()
                if commemt_id_new['commentId'] != 0:
                    self.write_str(u"1.0.2-1.2 添加评论之后,影响评论列表 success,耗时"+str(self.get_time_long(cn_numbers_time1,cn_numbers_time2)))
                    self.write_email_log('1.0.2-1.2',"添加评论之后,影响评论列表,耗时"+str(self.get_time_long(cn_numbers_time1,cn_numbers_time2)),"success")
                else:
                    self.write_str(u"1.0.2-1.2 添加评论之后,影响评论列表 fail")
                    self.write_email_log('1.0.2-1.2',"添加评论之后,影响评论列表","fail")

                # # 添加评论之后,影响媒体发布人的消息状态  
                # ================================= 3 ============================================ 
                cn_mes_time1=self.get_now_time()
                add_msgStatus = self.ants_get_msgStatus(pid)
                print(add_msgStatus)
                # print(add_msgStatus_init_pid[0]['commentCnt']
                # print(add_msgStatus[0]['commentCnt']
                cn_mes_time2=self.get_now_time()
                if add_msgStatus == -1 or add_msgStatus == -100:
                    self.write_str(u"1.0.2-1.3-1 添加评论之后,媒体发布人的消息状态列表出现异常 error")
                    self.write_email_log('1.0.2-1.3-1',"添加评论之后,媒体发布人的消息状态列表出现异常","error")
                elif add_msgStatus == False:
                    self.write_str(u"1.0.2-1.3-1 添加评论之后,影响媒体发布人的消息状态列表 fail")
                    self.write_email_log('1.0.2-1.3-1',"添加评论之后,影响媒体发布人的消息状态列表","fail")
                elif add_msgStatus[0]['commentCnt']==add_msgStatus_init_pid[0]['commentCnt']+1:
                    self.write_str(u"1.0.2-1.3-1 添加评论之后,影响媒体发布人的消息状态列表 success")
                    self.write_email_log('1.0.2-1.3-1',"添加评论之后,影响媒体发布人的消息状态列表","success")
                else:
                    self.write_str(u"1.0.2-1.3-1 添加评论之后,影响媒体发布人的消息状态列表 fail")
                    self.write_email_log('1.0.2-1.3-1',"添加评论之后,影响媒体发布人的消息状态列表","fail")


                # # 添加评论之后,影响媒体发布人的消息列表  
                # ================================= 3 ============================================ 
                cn_mes_time1=self.get_now_time()
                ax ={'commentContent': bodys['content']}
                add_msg = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                print(add_msg)
                cn_mes_time2=self.get_now_time()
                if add_msg == -1 or add_msg == -100:
                    self.write_str(u"1.0.2-1.3 添加评论之后,媒体发布人的消息列表出现异常 error")
                    self.write_email_log('1.0.2-1.3',"添加评论之后,媒体发布人的消息列表出现异常","error")
                elif add_msg == False:
                    self.write_str(u"1.0.2-1.3 添加评论之后,影响媒体发布人的消息列表 fail")
                    self.write_email_log('1.0.2-1.3',"添加评论之后,影响媒体发布人的消息列表","fail")
                else:
                    self.write_str(u"1.0.2-1.3 添加评论之后,影响媒体发布人的消息列表 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log('1.0.2-1.3',"添加评论之后,影响媒体发布人的消息列表,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")

                # # 添加评论之后,影响媒体发布人的回复人消息状态  
                # ================================= 3 ============================================ 
                cn_mes_time1=self.get_now_time()
                add_msgStatus_uid = self.ants_get_msgStatus(persons[2])
                print(add_msgStatus_uid)
                cn_mes_time2=self.get_now_time()
                if add_msgStatus_uid == -1 or add_msgStatus_uid == -100:
                    self.write_str(u"1.0.2-1.4-1 添加评论之后,回复人的消息状态列表出现异常 error")
                    self.write_email_log('1.0.2-1.4-1',"添加评论之后,回复人的消息状态列表出现异常","error")
                elif add_msgStatus_uid == False:
                    self.write_str(u"1.0.2-1.4-1 添加评论之后,回复人发布人的消息状态列表 fail")
                    self.write_email_log('1.0.2-1.4-1',"添加评论之后,回复人的消息状态列表","fail")
                elif add_msgStatus_uid[0]['commentCnt']==add_msgStatus_init_uid[0]['commentCnt']+1:
                    self.write_str(u"1.0.2-1.4-1 添加评论之后,回复人的消息状态列表 success")
                    self.write_email_log('1.0.2-1.4-1',"添加评论之后,回复人消息状态列表","success")
                else:
                    self.write_str(u"1.0.2-1.4-1 添加评论之后,回复人的消息状态列表 fail")
                    self.write_email_log('1.0.2-1.4-1',"添加评论之后,回复人的消息状态列表","fail")

                # # 添加评论之后,影响评价回复人的消息列表 
                # ================================= 4 ============================================
                cn_mes_reply_time1 =self.get_now_time()
                replyAdd_msg = self.ants_get_msg(mediaId,1,3,persons[1],ax,persons[2])
                print(replyAdd_msg)
                cn_mes_reply_time2 = self.get_now_time()
                if replyAdd_msg == -1 or replyAdd_msg == -100:
                    self.write_str(u"1.0.2-1.4 添加评论之后,评价回复人的消息列表出现异常 error")
                    self.write_email_log('1.0.2-1.4',"添加评论之后,评价回复人的消息列表出现异常","error")
                elif replyAdd_msg == False:
                    self.write_str(u"1.0.2-1.4 添加评论之后,影响评价回复人的消息列表 fail")
                    self.write_email_log('1.0.2-1.4',"添加评论之后,影响评价回复人的消息列表","fail")
                else:
                    self.write_str(u"1.0.2-1.4 添加评论之后,影响评价回复人的消息列表 success,耗时"+str(self.get_time_long(cn_mes_reply_time1,cn_mes_reply_time2)))
                    self.write_email_log('1.0.2-1.4',"添加评论之后,影响评价回复人的消息列表,耗时"+str(self.get_time_long(cn_mes_reply_time1,cn_mes_reply_time2)),"success")

                # # 添加评论之后,影响媒体发布人的分享列表 
                # ================================= 5 ============================================
                cn_share_time1=self.get_now_time()
                comments_count = self.ants_private_share(pid,'mediaId',mediaId,'comments',persons[1])
                print(comments_count)
                print(comments_count_init)
                cn_share_time2 =self.get_now_time()
                if comments_count== -1 or comments_count == -100:
                    self.write_str(u"1.0.2-1.5 添加评论之后,影响媒体发布人的分享列表异常 error")
                    self.write_email_log('1.0.2-1.5',"添加评论之后,影响媒体发布人的分享列表异常","error")
                elif comments_count[0]==comments_count_init[0]+1:
                    self.write_str(u"1.0.2-1.5 添加评论之后,影响媒体发布人的分享列表 success,耗时"+str(self.get_time_long(cn_share_time1,cn_share_time2)))
                    self.write_email_log('1.0.2-1.5',"添加评论之后,影响媒体发布人的分享列表,耗时"+str(self.get_time_long(cn_share_time1,cn_share_time2)),"success")
                else:
                    self.write_str(u"1.0.2-1.5 添加评论之后,影响媒体发布人的分享列表 fail")
                    self.write_email_log('1.0.2-1.5',"添加评论之后,影响媒体发布人的分享列表","fail")

                # # 添加评论之后,影响影响标签最新列表 
                # ================================ 6 =============================================
                if isRunTag:
                    cn_indexFollow_time1=self.get_now_time()
                    tag_least_comments = self.ants_tags_least(tagId,'mediaId',mediaId,'comments',persons[1])
                    tag_least_commentResList = self.ants_tags_least(tagId,'mediaId',mediaId,'commentResList',persons[1])
                    tag_cn_isIn=self.get_new_commentId(tag_least_commentResList_init,tag_least_commentResList)
                    print(str(tag_least_comments)+'+***'+str(len(tag_least_commentResList)))

                    cn_indexFollow_time2 = self.get_now_time()
                    if tag_least_comments[0]==(tag_least_comments_init[0]+1) and tag_cn_isIn != 0:
                        self.write_str(u"1.0.2-1.6 添加评论之后,影响标签"+str(tagId)+"最新列表 success,耗时"+str(self.get_time_long(cn_indexFollow_time1,cn_indexFollow_time2)))
                        self.write_email_log('1.0.2-1.6',"添加评论之后,影响标签"+str(tagId)+"最新列表,耗时"+str(self.get_time_long(cn_indexFollow_time1,cn_indexFollow_time2)),"success")
                    else:
                        self.write_str(u"1.0.2-1.6 添加评论之后,影响标签"+str(tagId)+"最新列表 fail")
                        self.write_email_log('1.0.2-1.6',"添加评论之后,影响标签"+str(tagId)+"最新列表","fail")

                # # 添加评论之后,影响首页列表 
                # ================================ 7 =============================================
                cn_find_time1 = self.get_now_time()
                index_comments = self.ants_index('mediaId',mediaId,'comments',pid)
                index_commentResList = self.ants_index('mediaId',mediaId,'commentResList',pid)
                index_cn_isIn = self.get_new_commentId(index_commentResList_init,index_commentResList)
                # print(str(index_comments)+'888'+str(len(index_commentResList))
                cn_find_time2 = self.get_now_time()
                if index_comments[0] == (index_comments_init[0]+1) and index_cn_isIn != 0:
                    self.write_str(u"1.0.2-1.7 添加评论之后,影响首页列表 success,耗时"+str(self.get_time_long(cn_find_time1,cn_find_time2)))
                    self.write_email_log('1.0.2-1.7',"添加评论之后,影响首页列表,耗时"+str(self.get_time_long(cn_find_time1,cn_find_time2)),"success")
                else:
                    self.write_str(u"1.0.2-1.7 添加评论之后,影响首页列表 fail")
                    self.write_email_log('1.0.2-1.7',"添加评论之后,影响首页列表","fail")

                # # 添加评论之后,影响俱乐部最新列表 
                # =============================== 8 ==============================================
                if isRunClub:
                    cn_city_time1=self.get_now_time()
                    comments_club = self.ants_club_latest(clubId,'mediaId',mediaId,'comments',pid)
                    commentResList_club = self.ants_club_latest(clubId,'mediaId',mediaId,'commentResList',pid)
                    if commentResList_club == -1 or commentResList_club == -100:
                        self.write_str(u"1.0.2-1.8 添加评论之后,俱乐部最新列表异常 fail")
                        self.write_email_log('1.0.2-1.8',"添加评论之后,俱乐部最新列表异常","fail")
                    else:  
                        club_cn_isIn = self.get_new_commentId(commentResList_club_init[0],commentResList_club[0])
                        print(commentResList_club)
                        print(commentResList_club_init)
                        print(club_cn_isIn)
                        cn_city_time2 =self.get_now_time()
                        if comments_club[0]==(comments_club_init[0]+1) and club_cn_isIn !=0:
                            self.write_str(u"1.0.2-1.8 添加评论之后,影响俱乐部最新列表 success,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)))
                            self.write_email_log('1.0.2-1.8',"添加评论之后,影响俱乐部最新列表,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)),"success")
                        else:
                            self.write_str(u"1.0.2-1.8 添加评论之后,影响俱乐部最新列表 fail")
                            self.write_email_log('1.0.2-1.8',"添加评论之后,影响俱乐部最新列表","fail")

                # 添加评论之后,影响点赞过的用户的喜欢列表 
                # ============================== 9 ===============================================
                if isRunlike:
                    cn_like_time1=self.get_now_time()
                    comments_count_like = self.ants_likeList(persons[2],'mediaId',mediaId,'comments',persons[1])
                    print(comments_count_like)
                    cn_like_time2 =self.get_now_time()
                    if comments_count_like ==-1 or comments_count_like == -100:
                        self.write_str(u"1.0.2-1.9 添加评论之后,影响点赞过的用户的喜欢列表异常 error")
                        self.write_email_log('1.0.2-1.9',"添加评论之后,影响点赞过的用户的喜欢列表异常","error")
                    elif comments_count_like == False:
                        self.write_str(u"1.0.2-1.9 添加评论之后,影响点赞过的用户的喜欢列表 fail")
                        self.write_email_log('1.0.2-1.9',"添加评论之后,影响点赞过的用户的喜欢列表","fail")
                    elif comments_count_like[0]==comments_count_like_init[0]+1:
                        self.write_str(u"1.0.2-1.9 添加评论之后,影响点赞过的用户的喜欢列表 success,耗时"+str(self.get_time_long(cn_like_time1,cn_like_time2)))
                        self.write_email_log('1.0.2-1.9',"添加评论之后,影响点赞过的用户的喜欢列表,耗时"+str(self.get_time_long(cn_like_time1,cn_like_time2)),"success")
                    else:
                        self.write_str(u"1.0.2-1.9 添加评论之后,影响点赞过的用户的喜欢列表 fail")
                        self.write_email_log('1.0.2-1.9',"添加评论之后,影响点赞过的用户的喜欢列表","fail")
        if isFalse:
            # ======================= 删除评论 ============================================================
            del_cn_time1=self.get_now_time()
            del_com=self.ants_del_comment(commemt_id['commentId'],mediaId,persons[1])
            del_cn_time2=self.get_now_time()
            if del_com == 'success':
                self.write_str(u"1.0.2-2 删除评论"+str(commemt_id['commentId'])+"成功！耗时"+str(self.get_time_long(del_cn_time1,del_cn_time2)))
                self.write_email_log('1.0.2-2',"删除评论"+str(commemt_id['commentId'])+" 耗时"+str(self.get_time_long(del_cn_time1,del_cn_time2)),'success')
            else:
                self.write_str(u"1.0.2-2 删除评论 fail")
                self.write_email_log('1.0.2-2',"删除评论","fail")

            time.sleep(5)
        if isFalse:
            # 删除评论之后,媒体详情  ================================== 1 ================================================
            cn_detail_end_time1 = self.get_now_time()
            comments_end = self.ants_media_detail(mediaId,persons[1])
            cn_end = comments_end[0]['comments']
            cmList_end = comments_end[0]['commentResList']
            # self.write_str(str(cn_end))
            # self.write_str(str(len(cmList_end)))
            cn_detail_end_time2 =self.get_now_time()
            # # 验证是否删除最新commentId
            isEqual = self.get_new_commentId(cmList,cmList_end)
            if isEqual==0 and cn==cn_end+1:
                self.write_str(u"1.0.2-2.1 删除影响媒体详情成功！最新commentId " + str(commemt_id['commentId'])+",comments:"+str(cn_end)+",耗时"+str(self.get_time_long(cn_detail_end_time1,cn_detail_end_time2)))
                self.write_email_log('1.0.2-2.1',"删除最新commentId " + str(commemt_id['commentId'])+",耗时"+str(self.get_time_long(cn_detail_end_time1,cn_detail_end_time2)),"success")
            else:
                self.write_str(u"1.0.2-2.1 删除最新commentId fail")
                self.write_email_log('1.0.2-2.1',"删除最新commentId " + str(commemt_id['commentId']),"fail")
   
            # # 删除评论之后,影响评论列表 
            # ============================== 2 =================================================
            cnList_end_time1=self.get_now_time()
            cn_numbers_end = self.ants_get_comments_list(mediaId,persons[1])
            print(cn_numbers_end)
            print(cn_numbers)
            cnList_end_time2 =self.get_now_time()
            isEqual_new = self.get_new_commentId(cn_numbers,cn_numbers_end)
            if isEqual_new==0:
                self.write_str(u"1.0.2-2.2 删除评论之后,影响评论列表 success,耗时"+str(self.get_time_long(cnList_end_time1,cnList_end_time2)))
                self.write_email_log('1.0.2-2.2',"删除评论之后,影响评论列表,耗时"+str(self.get_time_long(cnList_end_time1,cnList_end_time2)),"success")
            else:
                self.write_str(u"1.0.2-2.2 删除评论之后,影响评论列表 fail")
                self.write_email_log('1.0.2-2.2',"删除评论之后,影响评论列表","fail")

            # # 删除评论之后,影响媒体发布人的消息列表  
            # ============================= 3 ================================================== 
            cn_msg_end_time1=self.get_now_time()
            isDel_msg = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
            print(isDel_msg)
            cn_msg_end_time2=self.get_now_time()
            if isDel_msg == -1 or isDel_msg == -100:
                self.write_str(u"1.0.2-2.3 删除评论之后,媒体发布人的消息列表出现异常 error")
                self.write_email_log('1.0.2-2.3',"删除评论之后,媒体发布人的消息列表出现异常","error")
            elif isDel_msg == False:
                self.write_str(u"1.0.2-2.3 删除评论之后,清除已发出的评价消息 success,耗时"+str(self.get_time_long(cn_msg_end_time1,cn_msg_end_time2)))
                self.write_email_log('1.0.2-2.3',"删除评论之后,清除已发出的评价消息,耗时"+str(self.get_time_long(cn_msg_end_time1,cn_msg_end_time2)),"success")
            else:
                self.write_str(u"1.0.2-2.3 删除评论之后,清除已发出的评价消息 fail")
                self.write_email_log('1.0.2-2.3',"删除评论之后,清除已发出的评价消息","fail")
                

            # # 删除评论之后,影响评价回复人的消息列表 
            # ============================ 4 ===================================================
            cn_msg_end_replay_time1 =self.get_now_time()
            isReplyDel_msg = self.ants_get_msg(mediaId,1,3,persons[1],ax,persons[2])
            cn_msg_end_replay_time2 =self.get_now_time()
            if isReplyDel_msg == -1 or isReplyDel_msg == -100:
                self.write_str(u"1.0.2-2.4 删除评论之后,回复人的消息列表出现异常 error")
                self.write_email_log('1.0.2-2.4',"删除评论之后,回复人的消息列表出现异常","error")
            elif isReplyDel_msg == False:
                self.write_str(u"1.0.2-2.4 删除评论之后,清除已发出的回复消息 success,耗时"+str(self.get_time_long(cn_msg_end_replay_time1,cn_msg_end_replay_time2)))
                self.write_email_log('1.0.2-2.4',"删除评论之后,清除已发出的回复消息,耗时"+str(self.get_time_long(cn_msg_end_replay_time1,cn_msg_end_replay_time2)),"success")
            else:
                self.write_str(u"1.0.2-2.4 删除评论之后,清除已发出的回复消息 fail")
                self.write_email_log('1.0.2-2.4',"删除评论之后,清除已发出的回复消息","fail")

            # # 删除评论之后,影响媒体发布人的分享列表 
            # ============================ 5 ===================================================
            cn_share_end_time1 =self.get_now_time()
            comments_count_end = self.ants_private_share(pid,'mediaId',mediaId,'comments',persons[1])
            cn_share_end_time2 = self.get_now_time()
            if comments_count_end == -1 or comments_count_end == -100:
                self.write_str(u"1.0.2-2.5 删除评论之后,媒体发布人的分享列表异常 fail")
                self.write_email_log('1.0.2-2.5',"删除评论之后,媒体发布人的分享列表异常","fail")
            elif comments_count_end[0]==comments_count[0]-1:
                self.write_str(u"1.0.2-2.5 删除评论之后,影响媒体发布人的分享列表 success,耗时"+str(self.get_time_long(cn_share_end_time1,cn_share_end_time2)))
                self.write_email_log('1.0.2-2.5',"删除评论之后,影响媒体发布人的分享列表,耗时"+str(self.get_time_long(cn_share_end_time1,cn_share_end_time2)),"success")
            else:
                self.write_str(u"1.0.2-2.5 删除评论之后,影响媒体发布人的分享列表 fail")
                self.write_email_log('1.0.2-2.5',"删除评论之后,影响媒体发布人的分享列表","fail")

            # # 删除评论之后,影响标签最新列表
            # ============================ 6 ===================================================
            if isRunTag:
                cn_indexFollow_end_time1=self.get_now_time()
                tag_least_comments_end = self.ants_tags_least(tagId,'mediaId',mediaId,'comments',persons[1])
                tag_least_commentResList_end = self.ants_tags_least(tagId,'mediaId',mediaId,'commentResList',persons[1])
                if tag_least_commentResList_end == -1 or tag_least_commentResList_end == -100:
                    self.write_str(u"1.0.2-2.6 删除评论之后,标签"+str(tagId)+"最新列表异常 fail")
                    self.write_email_log('1.0.2-2.6',"删除评论之后,标签"+str(tagId)+"最新列表异常","fail")
                else:
                    tag_cn_isIn_end =self.get_new_commentId(tag_least_commentResList[0],tag_least_commentResList_end[0])
                    print(tag_least_commentResList[0])
                    print(tag_least_commentResList_end[0])
                    print(tag_cn_isIn_end)
                    print(tag_least_comments_end)
                    print(tag_least_comments_init)
                    cn_indexFollow_end_time2=self.get_now_time()
                    if tag_least_comments_end[0]==tag_least_comments[0]-1 and tag_cn_isIn_end ==0:
                        self.write_str(u"1.0.2-2.6 删除评论之后,影响标签"+str(tagId)+"最新列表 success,耗时"+str(self.get_time_long(cn_indexFollow_end_time1,cn_indexFollow_end_time2)))
                        self.write_email_log('1.0.2-2.6',"删除评论之后,影响标签"+str(tagId)+"最新列表,耗时"+str(self.get_time_long(cn_indexFollow_end_time1,cn_indexFollow_end_time2)),"success")
                    else:
                        self.write_str(u"1.0.2-2.6 删除评论之后,影响标签"+str(tagId)+"最新列表 fail")
                        self.write_email_log('1.0.2-2.6',"删除评论之后,影响标签"+str(tagId)+"最新列表","fail")

            # # 删除评论之后,影响首页列表 
            # =========================== 7 ====================================================
            cn_find_time1 = self.get_now_time()
            index_comments_end = self.ants_index('mediaId',mediaId,'comments',pid)
            index_commentResList_end = self.ants_index('mediaId',mediaId,'commentResList',pid)
            cn_find_time2 = self.get_now_time()
            if index_commentResList_end == -1 or index_commentResList_end == -100:
                self.write_str(u"1.0.2-2.7 删除评论之后,首页列表异常 fail")
                self.write_email_log('1.0.2-2.7',"删除评论之后,首页列表异常","fail")
            else:
                index_cn_isIn_end = self.get_new_commentId(index_commentResList[0],index_commentResList_end[0])
                print(index_comments_end)
                print(index_comments_init)
                print(index_cn_isIn_end)
                if index_comments_end[0] == index_comments[0]-1 and index_cn_isIn_end == 0:
                    self.write_str(u"1.0.2-2.7 删除评论之后,影响首页列表 success,耗时"+str(self.get_time_long(cn_find_time1,cn_find_time2)))
                    self.write_email_log('1.0.2-2.7',"删除评论之后,影响首页列表,耗时"+str(self.get_time_long(cn_find_time1,cn_find_time2)),"success")
                else:
                    self.write_str(u"1.0.2-2.7 删除评论之后,影响首页列表 fail")
                    self.write_email_log('1.0.2-2.7',"删除评论之后,影响首页列表","fail")

            # # 删除评论之后,影响俱乐部最新列表
            # =========================== 8 ====================================================
            if isRunClub:
                cn_city_end_time1=self.get_now_time()
                comments_club_end = self.ants_club_latest(clubId,'mediaId',mediaId,'comments',pid)
                commentResList_club_end = self.ants_club_latest(clubId,'mediaId',mediaId,'commentResList',pid)
                cn_city_end_time2 = self.get_now_time()
                if commentResList_club_end == -1 or commentResList_club_end == -100:
                    self.write_str(u"1.0.2-2.8 删除评论之后,俱乐部最新列表异常 fail")
                    self.write_email_log("1.0.2-2.8 ","除评论之后,俱乐部最新列表异常","fail")
                else:
                    club_cn_isIn_end=self.get_new_commentId(commentResList_club[0],commentResList_club_end[0])
                    print(comments_club_end)
                    print(comments_club_init)
                    print(type(club_cn_isIn_end),club_cn_isIn_end)
                    print(type(comments_club_end),comments_club_end)
                    print(type(comments_club_init),comments_club_init)
                    if comments_club_end[0]==comments_club[0]-1 and club_cn_isIn_end == 0:
                        self.write_str(u"1.0.2-2.8 删除评论之后,影响俱乐部最新列表 success,耗时"+str(self.get_time_long(cn_city_end_time1,cn_city_end_time2)))
                        self.write_email_log("1.0.2-2.8","删除评论之后,影响俱乐部最新列表,耗时"+str(self.get_time_long(cn_city_end_time1,cn_city_end_time2)),"success")
                    else:
                        self.write_str(u"1.0.2-2.8 删除评论之后,影响俱乐部最新列表 fail")
                        self.write_email_log("1.0.2-2.8","删除评论之后,影响俱乐部最新列表","fail")
            
            # 删除评论之后,影响点赞过的用户的喜欢列表 
            # ========================== 9 =====================================================
            if isRunlike:
                cn_like_end_time1=self.get_now_time()
                comments_count_like_end = self.ants_likeList(persons[2],'mediaId',mediaId,'comments',persons[1])
                print(comments_count_like_end)
                cn_like_end_time2=self.get_now_time()
                if comments_count_like_end == -1 or comments_count_like_end == -100:
                    self.write_str(u"1.0.2-2.9 删除评论之后点赞过的用户的喜欢列表异常 fail")
                    self.write_email_log("1.0.2-2.9","删除评论之后点赞过的用户的喜欢列表异常","fail")
                elif comments_count_like_end == False:
                    self.write_str(u"1.0.2-2.9 删除评论之后,影响点赞过的用户的喜欢列表 fail")
                    self.write_email_log("1.0.2-2.9","删除评论之后,影响点赞过的用户的喜欢列表","fail")
                elif comments_count_like_end[0]==comments_count_like[0]-1:
                    self.write_str(u"1.0.2-2.9 删除评论之后,影响点赞过的用户的喜欢列表 success,耗时"+str(self.get_time_long(cn_like_end_time1,cn_like_end_time2)))
                    self.write_email_log("1.0.2-2.9","删除评论之后,影响点赞过的用户的喜欢列表,耗时"+str(self.get_time_long(cn_like_end_time1,cn_like_end_time2)),"success")
                else:
                    self.write_str(u"1.0.2-2.9 删除评论之后,影响点赞过的用户的喜欢列表 fail")
                    self.write_email_log("1.0.2-2.9","删除评论之后,影响点赞过的用户的喜欢列表","fail")
                
            #取消点赞
            bodys['doLike'] = False
            status=self.ants_like(mediaId,bodys,persons[2])
            if status == 'success':
                self.write_str(u"取消点赞 success")

        # 结束测试
        self.close_fd()
        self.EndTest()

# ===================================================================================================
    #比较两次内容获取最新的commentId
    def get_new_commentId(self,comments_init_num,comments_num):
        if comments_init_num =='':
            comments_init_num=[]
        if comments_num=='':
            comments_num=[]

        for x in comments_num:
            if x not in comments_init_num:
                self.write_str("the newest comment id " + str(x))
                return x
                print(x)
        return 0

    def get_num_comment(self,comments):
        ax = []
        for i in range(len(comments)):
            ax.append(comments[i]['commentId'])
        return ax

# =====================================================================================================


def main():
    reload(sys)

    server,persons,serve_yy,server_firmware = inifile.get_input_params()

    case = Comment(server,serve_yy,"two")
    case.run_case(persons)


if __name__=="__main__":
    main()