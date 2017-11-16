# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/5/18
import os
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# print(crupath
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)
import inifile
import time

isRun = False

class Message(Common):

    def __init__(self,server,serve_yy,ModuleName):
        Common.__init__(self,server,serve_yy,ModuleName)
   
    def run_message_cases(self,persons):

        isRunComment = False

        result = self.get_mediaId()
        mediaId = int(result)
        print(mediaId)

        userId=self.get_pid()
        pid=int(userId)

        if mediaId != 0:
            isRun =True
            self.write_str(u"1.0.12 消息列表case")
            self.write_email_log('1.0.12',"消息列表case",'1')

        if isRun:
            self.write_str('=======删除评论消息=======')
            self.write_email_log('0000','=======删除评论消息=======','success')

            #添加评论
            add_cn_time1=self.get_now_time()
            bodys={}
            bodys['content'] = self.get_random() + ' === Good !===> '+ self.get_local_time()
            bodys['mediaId'] = mediaId
            add_reply_sult =self.ants_add_comment(mediaId,bodys,persons[1])
            add_cn_time2=self.get_now_time()

            if add_reply_sult =='success':

                time.sleep(5)

                #获取媒体创建用户的消息列表
                msg_time1=self.get_now_time()
                ax ={'commentContent': bodys['content']}
                com_noreply_other_add_result = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                msg_time2=self.get_now_time()
                print(com_noreply_other_add_result)
                print('===========')
                if com_noreply_other_add_result == -1 or com_noreply_other_add_result==-100:
                    self.write_str("1.0.12-1.1 添加评论未@用户后消息列表异常 error ")
                    self.write_email_log('1.0.12-1.1',"添加评论未@用户后消息列表异常","error")
                elif com_noreply_other_add_result==False:
                    self.write_str("1.0.12-1.1 添加评论未@用户，消息列表内无信息 fail ")
                    self.write_email_log('1.0.12-1.1',"添加评论未@用户，消息列表内无信息","fail")
                elif com_noreply_other_add_result['mediaId'] ==mediaId:
                    self.write_str("1.0.12-1.1 添加评论未@用户影响消息列表 success,耗时："+str(self.get_time_long(msg_time1,msg_time2)))
                    self.write_email_log('1.0.12-1.1',"添加评论未@用户影响消息列表,耗时："+str(self.get_time_long(msg_time1,msg_time2)),"success")

                    # 删除消息
                    del_com_msg =self.ants_del_msg(1,com_noreply_other_add_result['key'],pid)
                    if del_com_msg==-1 or del_com_msg==-100:
                        self.write_str("1.0.12-1.2 评论消息删除异常 error")
                        self.write_email_log('1.0.12-1.2'," 评论消息删除异常","error")
                    elif del_com_msg =='success':
                        self.write_str("1.0.12-1.2 评论消息删除 success")
                        self.write_email_log('1.0.12-1.2',"评论消息删除","success")

                        # 删除评论之后,影响媒体发布人的消息列表  
                        # ================================= 3 ============================================ 
                        cn_mes_time1=self.get_now_time()
                        com_noreply_other_del_result = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                        print(com_noreply_other_del_result)
                        cn_mes_time2=self.get_now_time()
                        if com_noreply_other_del_result == -1 or com_noreply_other_del_result == -100:
                            self.write_str(u"1.0.12-1.3 删除消息未@用户影响消息列表出现异常 error")
                            self.write_email_log('1.0.12-1.3',"删除消息未@用户影响消息列表出现异常","error")
                        elif com_noreply_other_del_result == False:
                            self.write_str(u"1.0.12-1.3 删除评消息未@用户影响消息列表 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                            self.write_email_log('1.0.12-1.3'," 删除消息未@用户影响消息列表,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                        else:
                            self.write_str(u"1.0.12-1.3 删除消息未@用户影响消息列表 fail")
                            self.write_email_log("1.0.12-1.3","删除消息未@用户影响消息列表","fail")

                    else:
                        self.write_str("1.0.12-1.2 评论消息删除 fail")
                        self.write_email_log("1.0.12-1.2","评论消息删除","fail")
                else:
                    self.write_str("1.0.12-1.1 添加评论未@用户影响消息列表 fail ")
                    self.write_email_log('1.0.12-1.1',"添加评论未@用户影响消息列表 ","fail")
            else:
                self.write_str("1.0.12-1.0 用户评论无@用户的评论信息 fail ")
                self.write_email_log('1.0.12-1.1',"用户评论无@用户的评论信息","fail")
            #------------------------------------------------------------------------------------------------

            #获取媒体详情
            comment_init = self.ants_media_detail(mediaId,persons[1])
            cn_init = comment_init[0]['comments']
            cmList_init = comment_init[0]['commentResList']

            #--------用户自己评论自己的媒体信息----2--------------------
            self.write_str('=======用户自己评论自己的媒体信息=======')
            self.write_email_log('0000','=======用户自己评论自己的媒体信息=======','success')

            add_cn_time3=self.get_now_time()
            #添加评论
            add_self_media=self.ants_add_comment(mediaId,bodys,pid)
            add_cn_time4=self.get_now_time()
            if add_self_media =='success':
                comments = self.ants_media_detail(mediaId,pid)
                cn = comments[0]['comments']
                cmList = comments[0]['commentResList']

                # 得到最新评价的commentId
                commemt_id = self.get_new_Id(cmList_init,cmList)
                if commemt_id[0]['commentId'] != 0 and cn==(cn_init+1):
                    self.write_str(u"1.0.12-2.0 添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id[0]['commentId'])+",评论后comments:"+str(cn)+",评论前comments:"+str(cn_init)+',耗时：'+str(self.get_time_long(add_cn_time3,add_cn_time4)))
                    self.write_email_log("1.0.12-2.0"," 添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id[0]['commentId'])+",comments:"+str(cn)+",评论前comments:"+str(cn_init)+',耗时：'+str(self.get_time_long(add_cn_time3,add_cn_time4)),'success')
                else:
                    self.write_str("1.0.12-2.0 添加评论最新评价的commentId " + str(commemt_id[0]['commentId'])+",评论后comments:"+str(cn)+",评论前comments:"+str(cn_init)+" fail")
                    self.write_email_log('1.0.12-2.0',"添加评论最新评价的commentId " + str(commemt_id[0]['commentId'])+",评论后comments:"+str(cn)+",评论前comments:"+str(cn_init),"fail")

                time.sleep(5)

                #获取媒体创建用户的消息列表，无更新
                cn_mes_time1=self.get_now_time()
                com_noreply_self_add_result = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                print(com_noreply_self_add_result)
                cn_mes_time2=self.get_now_time()
                if com_noreply_self_add_result == -1 or com_noreply_self_add_result == -100:
                    self.write_str(u"1.0.12-2.1-2 自己评价自己发布的媒体消息列表异常 fail")
                    self.write_email_log("1.0.12-2.1-2","自己评价自己发布的媒体消息列表异常","error")
                elif com_noreply_self_add_result == False:
                    self.write_str(u"1.0.12-2.1-2 自己评价自己发布的媒体未收到消息 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log("1.0.12-2.1-2","自己评价自己发布的媒体未收到消息,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-2.1-2 自己评价自己发布的媒体未收到消息 fail")
                    self.write_email_log("1.0.12-2.1-2","自己评价自己发布的媒体未收到消息","fail")

                # 删除评论
                self.ants_del_comment(commemt_id[0]['commentId'],mediaId,pid)
                time.sleep(5)

                #消息列表内无更新
                cn_mes_time1=self.get_now_time()
                com_noreply_self_del = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                print(com_noreply_self_del)
                cn_mes_time2=self.get_now_time()
                if com_noreply_self_del == -1 or com_noreply_self_del == -100:
                    self.write_str(u"1.0.12-2.2-2 删除自己的评论信息消息列表异常 fail")
                    self.write_email_log("1.0.12-2.2-2","删除自己的评论信息消息列表异常","error")
                elif com_noreply_self_del == False:
                    self.write_str(u"1.0.12-2.2-2 删除自己的评论信息未收到消息 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log("1.0.12-2.2-2","删除自己的评论信息未收到消息,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-2.2-2 删除自己的评论信息未收到消息 fail")
                    self.write_email_log("1.0.12-2.2-2","删除自己的评论信息未收到消息","fail")
            else:
                self.write_str("1.0.12-2.0 自己评价自己的媒体 fail ")
                self.write_email_log("1.0.12-2.0","自己评价自己的媒体","fail")
  
            #------------------------------------------------------------------------------------------------

            #--------用户自己在自己的媒体内回复他人----3--------------------
            self.write_str('=======用户自己在自己的媒体内回复他人=======')
            self.write_email_log('0000','=======用户自己在自己的媒体内回复他人=======','success')
            # 添加评论
            add_cn_time5=self.get_now_time()
            bodys['userId'] = persons[2]
            add_reply_self_result =self.ants_add_comment(mediaId,bodys,pid)
            add_cn_time6=self.get_now_time()
            if add_reply_self_result =='success':
                comments = self.ants_media_detail(mediaId,pid)
                cn = comments[0]['comments']
                cmList = comments[0]['commentResList']

                # 得到最新评价的commentId
                commemt_id = self.get_new_Id(cmList_init,cmList)
                if commemt_id[0]['commentId'] != 0 and cn==(cn_init+1):
                    self.write_str(u"1.0.12-3.0 添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id[0]['commentId'])+"，评论后comments:"+str(cn)+",评论前："+str(cn_init)+"耗时："+str(self.get_time_long(add_cn_time5,add_cn_time6)))
                    self.write_email_log("1.0.12-3.0","添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id[0]['commentId'])+",评论后comments:"+str(cn)+",评论前："+str(cn_init)+",耗时："+str(self.get_time_long(add_cn_time5,add_cn_time6)),"success")

                else:
                    self.write_str(u"1.0.12-3.0 添加评论影响媒体详情fail")
                    self.write_email_log("1.0.12-3.0"," 添加评论影响媒体详情","fail")

                time.sleep(5)

                #获取媒体创建用户的消息列表
                cn_mes_time1=self.get_now_time()
                com_noreply_self_add = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                print(com_noreply_self_add)
                cn_mes_time2=self.get_now_time()
                if com_noreply_self_add == -1 or com_noreply_self_add == -100:
                    self.write_str(u"1.0.12-3.1-2 自己回复自己发布的媒体消息列表异常 fail")
                    self.write_email_log("1.0.12-3.1-2","自己回复自己发布的媒体消息列表异常","error")
                elif com_noreply_self_add == False:
                    self.write_str(u"1.0.12-3.1-2 自己回复自己发布的媒体未收到消息 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log("1.0.12-3.1-2","自己回复自己发布的媒体未收到消息,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-3.1-2 自己回复自己发布的媒体未收到消息 fail")
                    self.write_email_log("1.0.12-3.1-2","自己回复自己发布的媒体未收到消息","fail")

                #获取回复用户的消息列表
                cn_mes_time1=self.get_now_time()
                com_reply_other_add = self.ants_get_msg(mediaId,1,3,pid,ax,persons[2])
                print(com_reply_other_add)
                cn_mes_time2=self.get_now_time()
                if com_reply_other_add == -1 or com_reply_other_add == -100:
                    self.write_str(u"1.0.12-3.2-2 获取回复用户的消息列表异常 fail")
                    self.write_email_log("1.0.12-3.2-2","获取回复用户的消息列表异常","error")
                elif com_reply_other_add == False:
                    self.write_str(u"1.0.12-3.2-2 获取回复用户的消息列表 fail")
                    self.write_email_log("1.0.12-3.2-2","获取回复用户的消息列表","fail")
                else:
                    self.write_str(u"1.0.12-3.2-2 获取回复用户的消息列表 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log("1.0.12-3.2-2","获取回复用户的消息列表,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")

                # 删除评论
                self.ants_del_comment(commemt_id[0]['commentId'],mediaId,pid)
                time.sleep(5)

                #获取回复用户的消息列表
                cn_mes_time1=self.get_now_time()
                com_reply_other_del= self.ants_get_msg(mediaId,1,3,persons[1],ax,persons[2])
                print(com_reply_other_del)
                cn_mes_time2=self.get_now_time()
                if com_reply_other_del == -1 or com_reply_other_del == -100:
                    self.write_str(u"1.0.12-3.3-2 获取回复用户的消息列表异常 error")
                    self.write_email_log("1.0.12-3.3-2","获取回复用户的消息列表异常","error")
                elif com_reply_other_del == False:
                    self.write_str(u"1.0.12-3.3-2 获取回复用户的消息列表 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log("1.0.12-3.3-2","获取回复用户的消息列表,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-3.3-2 获取回复用户的消息列表 fail")
                    self.write_email_log("1.0.12-3.3-2","获取回复用户的消息列表","fail")

            else:
                self.write_str("1.0.12-3.0 用户自己在自己的媒体内回复他人 fail ")
                self.write_email_log("1.0.12-3.0","用户自己在自己的媒体内回复他人","fail")
            
            #------------------------------------------------------------------------------------------------
            #--------a用户媒体内回复媒体创建人----4--------------------
            self.write_str("=======用户在媒体内回复媒体创建人，媒体创建人预期只收到回复信息========")
            self.write_email_log('0000',"=======用户在媒体内回复媒体创建人，媒体创建人预期只收到回复信息========","success")
            #添加评论
            add_cn_time7=self.get_now_time()
            bodys['userId'] = pid
            add_reply_other_result =self.ants_add_comment(mediaId,bodys,persons[1])
            add_cn_time8=self.get_now_time()
            print(add_reply_other_result)
            if add_reply_other_result =='success':
                comments = self.ants_media_detail(mediaId,persons[1])
                cn = comments[0]['comments']
                cmList = comments[0]['commentResList']

                # 得到最新评价的commentId
                commemt_id = self.get_new_Id(cmList_init,cmList)
                if commemt_id[0]['commentId'] != 0 and cn==(cn_init+1):
                    self.write_str(u"1.0.12-4.0 添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id[0]['commentId'])+",添加后comments:"+str(cn)+",添加前："+str(cn_init)+",耗时："+str(self.get_time_long(add_cn_time7,add_cn_time8)))
                    self.write_email_log("1.0.12-4.0","添加评论影响媒体详情成功！最新评价的commentId " + str(commemt_id[0]['commentId'])+",添加后comments:"+str(cn)+",添加前："+str(cn_init)+",耗时："+str(self.get_time_long(add_cn_time7,add_cn_time8)),"success")
                else:
                    self.write_str(u"1.0.12-4.0 添加评论最新评价的commentId " + str(commemt_id[0]['commentId'])+",添加后comments:"+str(cn)+",添加前："+str(cn_init)+"fail")
                    self.write_email_log("1.0.12-4.0","添加评论最新评价的commentId " + str(commemt_id[0]['commentId'])+",添加后comments:"+str(cn)+",添加前："+str(cn_init),"fail")

                time.sleep(5)

                #获取媒体创建用户的消息列表
                cn_mes_time1=self.get_now_time()
                com_self_add = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                print(com_self_add)
                cn_mes_time2=self.get_now_time()
                if com_self_add == -1 or com_self_add == -100:
                    self.write_str(u"1.0.12-4.1-2 媒体创建人预期不收到评论消息异常 error")
                    self.write_email_log("1.0.12-4.1-2"," 媒体创建人预期不收到评论消息异常","error")
                elif com_self_add == False:
                    self.write_str(u"1.0.12-4.1-2 媒体创建人预期不收到评论消息 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log('1.0.12-4.1-2',"媒体创建人预期不收到评论消息,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-4.1-2 媒体创建人预期不收到评论消息 fail")
                    self.write_email_log('1.0.12-4.1-2',"媒体创建人预期不收到评论消息","fail")

                #获取媒体创建用户的消息列表
                cn_mes_time1=self.get_now_time()
                com_reply_self_add = self.ants_get_msg(mediaId,1,3,persons[1],ax,pid)
                print(com_reply_self_add)
                cn_mes_time2=self.get_now_time()
                if com_reply_self_add == -1 or com_reply_self_add == -100:
                    self.write_str(u"1.0.12-4.2-2 媒体创建人收到回复消息异常 error")
                    self.write_email_log('1.0.12-4.2-2',"媒体创建人收到回复消息异常","error")
                elif com_reply_self_add != False:
                    self.write_str(u"1.0.12-4.2-2 媒体创建人收到回复消息 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log('1.0.12-4.2-2',"媒体创建人收到回复消息,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-4.2-2 媒体创建人收到回复消息 fail")
                    self.write_email_log('1.0.12-4.2-2',"媒体创建人收到回复消息","fail")

                # 删除评论
                self.ants_del_comment(commemt_id[0]['commentId'],mediaId,pid)
                time.sleep(5)

                #获取媒体创建用户的消息列表
                cn_mes_time1=self.get_now_time()
                com_reply_self_add = self.ants_get_msg(mediaId,1,3,persons[1],ax,pid)
                print(com_reply_self_add)
                cn_mes_time2=self.get_now_time()
                if com_reply_self_add == -1 or com_reply_self_add == -100:
                    self.write_str(u"1.0.12-4.3-2 媒体创建人预期不收到评论消息异常 error")
                    self.write_email_log('1.0.12-4.3-2',"媒体创建人预期不收到评论消息异常","error")
                elif com_reply_self_add == False:
                    self.write_str(u"1.0.12-4.3-2 媒体创建人预期不收到评论消息 success,耗时"+str(self.get_time_long(cn_mes_time1,cn_mes_time2)))
                    self.write_email_log('1.0.12-4.3-2',"媒体创建人预期不收到评论消息,耗时" +str(self.get_time_long(cn_mes_time1,cn_mes_time2)),"success")
                else:
                    self.write_str(u"1.0.12-4.3-2 媒体创建人预期不收到评论消息 fail")
                    self.write_email_log('1.0.12-4.3-2',"媒体创建人预期不收到评论消息","fail")

            else:
                self.write_str("1.0.12-4.0 用户媒体内回复媒体创建人 fail")
                self.write_email_log('1.0.12-4.0',"用户媒体内回复媒体创建人","fail")
            #------------------------------------------------------------------------------------------------

        if isRun:
            self.write_str('==============点赞消息的删除=============')
            self.write_email_log('0000','==============点赞消息的删除=============','success')

            islike = self.ants_likeList(persons[1],'mediaId',mediaId,'mediaId',persons[1])
            if islike==False:
                #点赞
                like_time1=self.get_now_time()
                # 点赞
                bodys = {}
                bodys['mediaId'] = mediaId
                bodys['doLike'] = True
                likeStatus=self.ants_like(mediaId,bodys,persons[1])
                like_time2=self.get_now_time()
                if likeStatus=='success':
                    self.write_str(u"1.0.12_5.0 点赞 success,耗时"+str(self.get_time_long(like_time1,like_time2)))
                    self.write_email_log('1.0.12_5.0',"点赞,耗时"+str(self.get_time_long(like_time1,like_time2)),"success")
                else:
                    self.write_str(u"1.0.12_5.0 点赞 fail")
                    self.write_email_log('1.0.12_5.0',"点赞","fail")
            time.sleep(5)
            
            # # 点赞之后,影响媒体发布用户查看消息列表 
            # =============================================== 9 ======================================
            like_msg_time1=self.get_now_time()
            ax ={}
            isResultMediaGetlist = self.ants_get_msg(mediaId,3,5,persons[1],ax,pid)
            like_msg_time2=self.get_now_time()
            if isResultMediaGetlist == -1 or isResultMediaGetlist == -100:
                self.write_str(u"1.0.12_5.1 点赞之后,影响媒体发布用户查看消息列表出现异常 error")
                self.write_email_log('1.0.12_5.1',"点赞之后,影响媒体发布用户查看消息列表出现异常","error")
            elif isResultMediaGetlist == False:
                self.write_str(u"1.0.12_5.1 点赞之后,影响媒体发布用户查看消息列表 fail")
                self.write_email_log('1.0.12_5.1',"点赞之后,影响媒体发布用户查看消息列表","fail")
            else:
                self.write_str(u"1.0.12_5.1 点赞之后,影响媒体发布用户查看消息列表 success,耗时"+str(self.get_time_long(like_msg_time1,like_msg_time2)))
                self.write_email_log('1.0.12_5.1',"点赞之后,影响媒体发布用户查看消息列表,耗时"+str(self.get_time_long(like_msg_time1,like_msg_time2)),"success")

                #删除消息
                del_like_msg =self.ants_del_msg(3,isResultMediaGetlist['key'],pid)
                if del_like_msg==-1 or del_like_msg==-100:
                    self.write_str("1.0.12-5.2 点赞消息删除异常 error")
                    self.write_email_log('1.0.12-5.2',"点赞消息删除异常","error")
                elif del_like_msg =='success':
                    self.write_str("1.0.12-5.2 点赞消息删除 success")
                    self.write_email_log('1.0.12-5.2',"点赞消息删除","success")

                    time.sleep(5)

                    ## # 点赞之后,影响媒体发布用户查看消息列表 
                    # =============================================== 9 ======================================
                    like_msg_time1=self.get_now_time()
                    ax ={}
                    isResultMediaGetlist = self.ants_get_msg(mediaId,3,5,persons[1],ax,pid)
                    like_msg_time2=self.get_now_time()
                    if isResultMediaGetlist == -1 or isResultMediaGetlist == -100:
                        self.write_str(u"1.0.12_5.3 点赞消息删除之后,影响媒体发布用户查看消息列表出现异常 error")
                        self.write_email_log('1.0.12_5.3',"点赞消息删除之后,影响媒体发布用户查看消息列表出现异常","error")
                    elif isResultMediaGetlist == False:
                        self.write_str(u"1.0.12_5.3 点赞消息删除之后,影响媒体发布用户查看消息列表 success,耗时"+str(self.get_time_long(like_msg_time1,like_msg_time2)))
                        self.write_email_log('1.0.12_5.3',"点赞消息删除之后,影响媒体发布用户查看消息列表,耗时"+str(self.get_time_long(like_msg_time1,like_msg_time2)),"success")
                    else:
                        self.write_str(u"1.0.12_5.3 点赞消息删除之后,影响媒体发布用户查看消息列表 fail")
                        self.write_email_log('1.0.12_5.3',"点赞消息删除之后,影响媒体发布用户查看消息列表","fail")
                else:
                    self.write_str("1.0.12-5.2 点赞消息删除 fail")
                    self.write_email_log('1.0.12-5.2',"点赞消息删除","fail")

        if isRun:
            self.write_str('==============关注消息的删除=============')
            self.write_email_log('0000','==============关注消息的删除=============','success')

            isFollowListEnd = self.ants_fllowList(pid,1,persons[1])
            print(isFollowListEnd)
            if isFollowListEnd == False:

                # 添加关注 ==================================
                add_time1=self.get_now_time()
                isAddFollow = self.ants_follow(pid,1,persons[1])
                add_time2=self.get_now_time()
                print(isAddFollow)
                if isAddFollow == 'success':
                    self.write_str(u"1.0.12_6.0 添加关注 success，耗时"+str(self.get_time_long(add_time1,add_time2)))
                    self.write_email_log('1.0.12_6.0'," 添加关注，耗时"+str(self.get_time_long(add_time1,add_time2)),"success")
                else:
                    self.write_str(u"1.0.12_6 添加关注 fail")
                    self.write_email_log('1.0.12_6',"添加关注","fail")
                time.sleep(5)

            # 添加关注之后,影响被关注用户的消息列表 
            # ======================================== 6 =======================================
            msg_time1=self.get_now_time()
            ax ={}
            isMediaGetlist = self.ants_get_msg(0,2,4,persons[1],ax,pid)
            print(isMediaGetlist)
            msg_time2=self.get_now_time()
            if isMediaGetlist == -1 or isMediaGetlist == -100:
                self.write_str(u"1.0.12_6.1 添加关注之后,被关注用户的消息列表异常 error")
                self.write_email_log('1.0.12_6.1',"添加关注之后,被关注用户的消息列表异常","error")
            elif isMediaGetlist == False:
                self.write_str(u"1.0.12_6.1 添加关注之后,影响被关注用户的消息列表 fail")
                self.write_email_log('1.0.12_6.1',"添加关注之后,影响被关注用户的消息列表","fail")
            else:
                self.write_str(u"1.0.12_6.1 添加关注之后,影响被关注用户的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                self.write_email_log('1.0.12_6.1',"添加关注之后,影响被关注用户的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")

                #删除消息
                del_like_msg =self.ants_del_msg(4,isMediaGetlist['key'],pid)
                if del_like_msg==-1 or del_like_msg==-100:
                    self.write_str("1.0.12_6.2 点赞消息删除异常 error")
                    self.write_email_log('1.0.12_6.2',"点赞消息删除异常","error")
                elif del_like_msg =='success':
                    self.write_str("1.0.12_6.2 点赞消息删除 success")
                    self.write_email_log('1.0.12_6.2',"点赞消息删除","success")

                # 添加关注之后,影响被关注用户的消息列表 
                # ======================================== 6 =======================================
                msg_time1=self.get_now_time()
                ax ={}
                isMediaGetlist = self.ants_get_msg(0,2,4,persons[1],ax,pid)
                print(isMediaGetlist)
                msg_time2=self.get_now_time()
                if isMediaGetlist == -1 or isMediaGetlist == -100:
                    self.write_str(u"1.0.12_6.3 添加关注之后,被关注用户的消息列表异常 error")
                    self.write_email_log('1.0.12_6.3',"添加关注之后,被关注用户的消息列表异常","error")
                elif isMediaGetlist == False:
                    self.write_str(u"1.0.12_6.3 添加关注之后,影响被关注用户的消息列表 success，耗时"+str(self.get_time_long(msg_time1,msg_time2)))
                    self.write_email_log('1.0.12_6.3',"添加关注之后,影响被关注用户的消息列表，耗时"+str(self.get_time_long(msg_time1,msg_time2)),"success")
                else:
                    self.write_str(u"1.0.12_6.3 添加关注之后,影响被关注用户的消息列表 fail")
                    self.write_email_log('1.0.12_6.3',"添加关注之后,影响被关注用户的消息列表","fail")

                #取消测试数据
                bodys['doLike'] = False
                self.ants_like(mediaId,bodys,persons[1])
                self.ants_follow(pid,0,persons[1])

        #结束测试
        self.close_fd()
        self.EndTest()


def main():
    reload(sys)

    
    server,persons,serve_yy,server_firmware = inifile.get_input_params()
    cases = Message(server,serve_yy,"seven")
    cases.run_message_cases(persons)


if __name__=="__main__":
    main()