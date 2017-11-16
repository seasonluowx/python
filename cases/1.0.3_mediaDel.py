#coding: UTF-8
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

class PubDel(Common):

    def __init__(self,server,serve_yy,ModuleName):
        Common.__init__(self,server,serve_yy,ModuleName)

    def run_cases(self,persons):
        isRunLike = False
        isRunComment =False
        isRun = False  
        isRunTag=False
        isRunClub=False  
        
        result = self.get_mediaId()
        print(result)
        mediaId = int(result)

        if mediaId != 0:
            isRun = True
            pass

        userId=self.get_pid()
        pid=int(userId)

        if isRun:      
            # 影响个人信息列表==========1.0.3——1.5===================
            userInfo_result = self.ants_get_user_info(pid,'shares',pid)
            print(userInfo_result)

            # 添加评论之前,媒体详情  
            # ============================== 1 ==========================================
            mediaInfo_init = self.ants_media_detail(mediaId,persons[1])
            #获取tag信息
            tags = mediaInfo_init[0]['tags']
            if tags != '':
                tagIds=tags.split(",")
                tagId=tagIds[0]
                isRunTag =True
                print('tagId:'+str(tagId))
            #获取club信息   
            tagList_init = mediaInfo_init[0]['tagList']
            for x in range(len(tagList_init)):
                if tagList_init[x]['mediaSpecial'] == 10:
                    clubId=tagList_init[x]['id']
                    isRunClub =True
                    print('clubId:'+str(clubId))

            # 影响点赞用户的喜欢列表==========1.0.3——1.6===================
            islike = self.ants_likeList(persons[1],'mediaId',mediaId,'mediaId',persons[1])
            print(islike)
            if islike==False:
                # 粉丝点赞
                like_time1 =self.get_now_time()
                bodys = {}
                bodys['mediaId'] = mediaId
                bodys['doLike'] = True
                likeStatus=self.ants_like(mediaId,bodys,persons[1])
                like_time2 =self.get_now_time()
                if likeStatus == 'success':
                    self.write_str('1.0.3 '+str(mediaId)+'点赞 success,耗时'+str(self.get_time_long(like_time1,like_time2)))
                    self.write_email_log('1.0.3 ',str(mediaId)+'点赞,耗时'+str(self.get_time_long(like_time1,like_time2)),'success')
                    isRunLike = True
                    time.sleep(5)

                    # 影响点赞用户个人信息列表==========1.0.3——1.5===================
                    result_userInfo_like_init = self.ants_get_user_info(persons[1],'likes',pid)
                else:
                    self.write_str('1.0.3 点赞'+str(mediaId)+'fail')
                    self.write_email_log('1.0.3 ','点赞'+str(mediaId),'fail')

            # 添加评论==========1.0.3——1.6===================
            cn_time1=self.get_now_time()
            bodys = {}
            bodys['content'] = self.get_random() + ' === Good !===> '+ self.get_local_time()
            bodys['mediaId'] = mediaId
            bodys['userId'] = persons[2]
            commentStatus = self.ants_add_comment(mediaId,bodys,persons[1])
            cn_time2=self.get_now_time()
            if commentStatus == 'success':
                self.write_str('1.0.3 添加'+str(mediaId)+'评论 success,耗时'+str(self.get_time_long(cn_time1,cn_time2)))
                self.write_email_log('1.0.3 ','添加'+str(mediaId)+'评论 ,耗时'+str(self.get_time_long(cn_time1,cn_time2)),'success')
                isRunComment = True
                time.sleep(5)
            else:
                self.write_str('1.0.3 添加'+str(mediaId)+'评论 fail')
                self.write_email_log('1.0.3 ','添加'+str(mediaId)+'评论','fail')

            #发布影响我关注的人发布的媒体列表
            isFollowList = self.ants_fllowList(pid,1,persons[1])
            print(isFollowList)
            if isFollowList == False:
                #添加关注
                self.ants_follow(pid,1,persons[1])
                time.sleep(5)
            newShare = self.ants_media_followNewShare('result',persons[1])
            print('newShare:'+str(newShare))

        
        if isRun: 
            #删除媒体
            del_time1 =self.get_now_time()
            deleteMedia_result = self.ants_delete_media(mediaId,pid)
            del_time2=self.get_now_time()
            if deleteMedia_result =='success':
                self.write_str('1.0.3 删除媒体'+str(mediaId)+'success，耗时'+str(self.get_time_long(del_time1,del_time2)))
                self.write_email_log('1.0.3 ','删除媒体'+str(mediaId)+'success，耗时'+str(self.get_time_long(del_time1,del_time2)),'success')
            else:
                self.write_str('1.0.3 删除媒体'+str(mediaId)+'fail')
                self.write_email_log('1.0.3 ','删除媒体'+str(mediaId),'fail')
            time.sleep(5)

        if isRun:
            # 影响首页列表==========1.0.1——1===================
            del_find_time1 =self.get_now_time()
            find_result = self.ants_index('mediaId',mediaId,'mediaId',pid)
            print(find_result)
            del_find_time2=self.get_now_time()
            if find_result == False:
                self.write_str(u"1.0.3-1 删除媒体影响首页列表 success，耗时"+str(self.get_time_long(del_find_time1,del_find_time2)))
                self.write_email_log(u"1.0.3-1","删除媒体影响首页列表，耗时"+str(self.get_time_long(del_find_time1,del_find_time2)),"success")
            else:
                self.write_str(u"1.0.3-1 删除媒体影响首页列表 fail")
                self.write_email_log(u"1.0.3-1","删除媒体影响首页列表","fail")

             # 影响影响俱乐部最新列表==========1.0.1——2===================
            if isRunClub:
                cn_city_time1=self.get_now_time()
                media_club = self.ants_club_latest(clubId,'mediaId',mediaId,'mediaId',persons[1])
                cn_city_time2 =self.get_now_time()
                if media_club==False:
                    self.write_str(u"1.0.3-2 删除媒体影响俱乐部最新列表 success,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)))
                    self.write_email_log(u"1.0.3-2","删除媒体影响俱乐部最新列表,耗时"+str(self.get_time_long(cn_city_time1,cn_city_time2)),"success")
                else:
                    self.write_str(u"1.0.3-2 删除媒体影响俱乐部最新列表 fail")
                    self.write_email_log(u"1.0.3-2","删除媒体点赞之后,影响俱乐部最新列表","fail")

            # # 影响标签最新列表==========1.0.1——3===================
            if isRunTag:
                like_indexFollow_time1=self.get_now_time()
                result_tag = self.ants_tags_least(tagId,'mediaId',mediaId,'mediaId',persons[1])
                like_indexFollow_time2=self.get_now_time()
                if result_tag==False:
                    self.write_str(u"1.0.3-3 删除媒体影响标签最新列表 success,耗时"+str(self.get_time_long(like_indexFollow_time1,like_indexFollow_time2)))
                    self.write_email_log(u"1.0.3-3","删除媒体影响标签最新列表,耗时"+str(self.get_time_long(like_indexFollow_time1,like_indexFollow_time2)),"success")
                else:
                    self.write_str(u"1.0.3-3 删除媒体影响标签最新列表 fail")
                    self.write_email_log(u"1.0.3-3","删除媒体影响标签最新列表","fail")

            # 影响个人分享列表======1.0.3——4======
            del_private_time1=self.get_now_time()
            share_result = self.ants_private_share(pid,'mediaId',mediaId,'mediaId',pid)
            del_private_time2=self.get_now_time()
            if share_result ==False :
                self.write_str(u"1.0.3—4 删除媒体影响媒体创建人个人分享列表 success，耗时"+str(self.get_time_long(del_private_time1,del_private_time2)))
                self.write_email_log(u"1.0.3—4","删除媒体影响媒体创建人个人分享列表，耗时"+str(self.get_time_long(del_private_time1,del_private_time2)),"success")
            else:
                self.write_str(u"1.0.3—4 删除媒体影响媒体创建人个人分享列表 fail")
                self.write_email_log(u"1.0.3—4","删除媒体影响媒体创建人个人分享列表","fail")  
        
            # 影响个人信息列表==========1.0.3——5===================
            del_userInfo_time1=self.get_now_time()
            userInfo_result_end = self.ants_get_user_info(pid,'shares',pid)
            print(userInfo_result_end)
            del_userInfo_time2=self.get_now_time()
            if userInfo_result_end == (userInfo_result-1):
                self.write_str(u"1.0.3-5 删除媒体影响媒体创建人个人信息列表shares-1 success,耗时"+str(self.get_time_long(del_userInfo_time1,del_userInfo_time2)),)
                self.write_email_log(u"1.0.3-5","删除媒体影响媒体创建人个人信息列表shares-1,耗时"+str(self.get_time_long(del_userInfo_time1,del_userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.3-5 删除媒体影响媒体创建人个人信息列表shares-1 ，删除前shares:"+str(userInfo_result)+",删除后shares："+str(userInfo_result_end)+" fail")
                self.write_email_log(u"1.0.3-5","删除媒体影响媒体创建人个人信息列表shares-1,，删除前shares:"+str(userInfo_result)+",删除后shares："+str(userInfo_result_end),"fail")     
            
            
            # 影响点赞用户的喜欢列表==========1.0.3——6===================
            del_likeList_time1=self.get_now_time()
            like_end = self.ants_likeList(persons[1],'mediaId',mediaId,'likes',pid)  
            del_likeList_time2=self.get_now_time()
            print(like_end)
            if like_end ==False:
                self.write_str(u"1.0.3-6 删除媒体影响点赞用户的喜欢列表 success，耗时"+str(self.get_time_long(del_likeList_time1,del_likeList_time2)))
                self.write_email_log(u"1.0.3-6"," 删除媒体影响点赞用户的喜欢列表，耗时"+str(self.get_time_long(del_likeList_time1,del_likeList_time2)),"success")
            else:
                self.write_str(u"1.0.3-6 删除媒体影响点赞用户的喜欢列表 fail")
                self.write_email_log(u"1.0.3-6"," 删除媒体影响点赞用户的喜欢列表","fail")
                
            if isRunLike:
                # 影响点赞用户的个人信息列表==========1.0.3——7===================
                del_userInfo_time3=self.get_now_time()
                result_userInfo_like_end = self.ants_get_user_info(persons[1],'likes',pid)
                del_userInfo_time4=self.get_now_time()

                if result_userInfo_like_init == result_userInfo_like_end+1:
                    self.write_str(u"1.0.3-7 删除媒体影响点赞用户个人信息 success，耗时"+str(self.get_time_long(del_userInfo_time3,del_userInfo_time4)))
                    self.write_email_log(u"1.0.3-7"," 删除媒体影响点赞用户个人信息，耗时"+str(self.get_time_long(del_userInfo_time3,del_userInfo_time4)),"success")
                else:
                    self.write_str(u"1.0.3-7 删除媒体影响点赞用户个人信息 fail")
                    self.write_email_log(u"1.0.3-7"," 删除媒体影响点赞用户个人信息","fail")

                
                # 影响媒体创建用户的点赞通知列表==========1.0.3——9===================
                del_msg_time1=self.get_now_time()
                ax={}
                isResultMediaGetlistEnd = self.ants_get_msg(mediaId,3,5,persons[1],ax,pid)
                del_msg_time2=self.get_now_time()
                if not isResultMediaGetlistEnd:
                    self.write_str(u"1.0.3-9 删除媒体影响媒体发布用户查看消息列表 success，耗时"+str(self.get_time_long(del_msg_time1,del_msg_time2)))
                    self.write_email_log(u"1.0.3-9"," 删除媒体影响媒体发布用户查看消息列表，耗时"+str(self.get_time_long(del_msg_time1,del_msg_time2)),"success")
                else:
                    self.write_str(u"1.0.3-9 删除媒体影响媒体发布用户查看消息列表 fail")
                    self.write_email_log(u"1.0.3-9"," 删除媒体影响媒体发布用户查看消息列表","fail")

            if isRunComment:
                # # 影响媒体,影响媒体发布人的消息列表  
                # ============================= 11================================================== 
                del_msg_time3=self.get_now_time()
                ax ={'commentContent': bodys['content']}
                isDel = self.ants_get_msg(mediaId,1,2,persons[1],ax,pid)
                del_msg_time4=self.get_now_time()
                if not isDel:
                    self.write_str(u"1.0.3-11 删除媒体影响媒体发布人的评论消息 success，耗时"+str(self.get_time_long(del_msg_time3,del_msg_time4)))
                    self.write_email_log(u"1.0.3-11"," 删除媒体影响媒体发布人的评论消息，耗时"+str(self.get_time_long(del_msg_time3,del_msg_time4)),"success")
                else:
                    self.write_str(u"1.0.3-11 删除媒体影响媒体发布人的评论消息 fail")
                    self.write_email_log(u"1.0.3-11"," 删除媒体影响媒体发布人的评论消息","fail")

                # # 影响媒体,影响评价回复人的消息列表 
                # ============================ 12 ===================================================
                del_msg_time5=self.get_now_time()
                isReplyDel = self.ants_get_msg(mediaId,1,3,persons[1],ax,persons[2])
                del_msg_time6=self.get_now_time()
                if not isReplyDel:
                    self.write_str(u"1.0.3-1.12 删除媒体影响评论回复人的消息列表 success，耗时"+str(self.get_time_long(del_msg_time5,del_msg_time6)))
                    self.write_email_log(u"1.0.3-1.12"," 删除媒体影响评论回复人的消息列表，耗时"+str(self.get_time_long(del_msg_time5,del_msg_time6)),"success")
                else:
                    self.write_str(u"1.0.3-1.12 删除媒体影响评论回复人的消息列表 fail")
                    self.write_email_log(u"1.0.3-1.12"," 删除媒体影响评论回复人的消息列表","fail")

            # 发布影响我关注的人发布的媒体列表==========1.0.1——1.7===================
            userInfo_time1=self.get_now_time()
            newShare_end = self.ants_media_followNewShare('result',persons[1])
            print('删除媒体之后，result：'+str(newShare_end)+'删除媒体之前，result：'+str(newShare))
            userInfo_time2=self.get_now_time()
            if newShare_end==-1 or newShare_end == -100:
                self.write_str("1.0.3-1.13 删除媒体之后,我关注的人发布的媒体列表出现异常了")
                self.write_email_log("1.0.3-1.13"," 发删除媒体之后,我关注的人发布的媒体列表出现异常了","error")
            elif newShare_end== (newShare-1):
                self.write_str(u"1.0.3-1.13 删除媒体之后,影响我关注的人发布的媒体列表 success,耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.3-1.13"," 删除媒体之后,影响我关注的人发布的媒体列表,耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.3-1.13 删除媒体之后,影响我关注的人发布的媒体列表 fail")
                self.write_email_log(u"1.0.3-1.13"," 删除媒体之后,影响我关注的人发布的媒体列表,result："+str(newShare_end)+"删除媒体之前，result："+str(newShare),"fail")

        #发布媒体
        if True:
            # 获取发布中body下的file Id值, 二
            fileId,mediaUrl,thumbUrl,uploadMethod = self.ants_get_media_fileId(1,pid)
            if fileId != '':
                # 完成媒体上传,五
                media = 'final.mp4'
                thumb = 'mao.jpg'            
                result=''
                for x in range(1,5):
                    publish_time3 =self.get_now_time()
                    isUpLoad = self.ants_upload_local_video_work(mediaUrl,media,thumbUrl,thumb)
                    publish_time4 =self.get_now_time()
                    if isUpLoad ==True:
                        print(isUpLoad)
                        self.write_str(u"1.0.3-2 第"+str(x)+"次上传视频 success,耗时："+str(self.get_time_long(publish_time3,publish_time4)))
                        self.write_email_log(u"1.0.3-2"," 第"+str(x)+"次上传视频耗时："+str(self.get_time_long(publish_time3,publish_time4)),'success')

                        # 发布媒体 ，五
                        #发布
                        bodys = {}
                        bodys['fileId'] = fileId
                        bodys['width'] = 1000
                        bodys['height'] = 1000
                        bodys['length'] = 10
                        bodys['pixelLevel']=3#0;//缺省1;//<720P 2;//>=720P3;//>=1080P
                        bodys['size'] = 7178
                        bodys['mediaType'] = 1
                        bodys['mediaMemo'] = 'publish video test'
                        bodys['exIf'] = 'id 3'
                        bodys['latitude'] = 31.555502
                        bodys['longitude'] = 121.256352 
                        bodys['locationDesc'] = '上海浦东新区，长泰广场'
                        bodys['urlType'] =uploadMethod

                        result = self.ants_publish_media(bodys,'v3.7',pid)
                        publish_time2 =self.get_now_time()
                        
                        if result != 0:
                            self.write_str(u"1.0.3-2 发布视频媒体 success")
                            self.write_email_log(u"1.0.3-2"," 发布视频媒体",'success')
                        else:
                            self.write_str(u"1.0.3-2 发布视频媒体 fail")
                            self.write_email_log(u"1.0.3-2"," 发布视频媒体",'fail')
                        break
                    else:
                        self.write_str(u"1.0.3-2 第"+str(x)+"次上传视频 fail")
                        self.write_email_log(u"1.0.3-2"," 第"+str(x)+"次上传视频",'fail')
                        continue
                         
            else:
                self.write_str(u"1.0.3-2 获取媒体发布url fail")
                self.write_email_log(u"1.0.3-2"," 获取媒体发布url",'fail')

            # 添加评论之前,媒体详情  
            # ============================== 1 ==========================================
            mediaInfo_init = self.ants_media_detail(result,persons[1])
            print(mediaInfo_init)
            if mediaInfo_init ==-1 or mediaInfo_init ==-100:
                self.write_str(u"1.0.3-2.1 视频发布之后，媒体详情访问异常 error")
                self.write_email_log(u"1.0.3-2.1"," 视频发布之后，媒体详情访问异常",'error')
            elif mediaInfo_init[0]['status'] ==0:
                self.write_str(u"1.0.3-2.1 视频发布之后，媒体详情 success")
                self.write_email_log(u"1.0.3-2.1"," 视频发布之后，媒体详情",'success')
            else:
                self.write_str(u"1.0.3-2.1 视频发布之后，媒体详情 fail")
                self.write_email_log(u"1.0.3-2.1"," 视频发布之后，媒体详情",'fail')

            #视频列表
            isRecomm_vlist = self.ants_video_index('mediaId',result,'mediaId',pid)
            print(isRecomm_vlist)
            if isRecomm_vlist ==-1 or isRecomm_vlist ==-100:
                self.write_str(u"1.0.3-2.2 视频发布之后，视频列表访问异常 error")
                self.write_email_log(u"1.0.3-2.2"," 视频发布之后，视频列表访问异常",'error')
            elif isRecomm_vlist[0] == result:
                self.write_str(u"1.0.3-2.2 视频发布之后，视频列表 success")
                self.write_email_log(u"1.0.3-2.2"," 视频发布之后，视频列表",'success')
            else:
                self.write_str(u"1.0.3-2.2 视频发布之后，视频列表 fail")
                self.write_email_log(u"1.0.3-2.2 ","视频发布之后，视频列表",'fail')

            #个人分享列表
            share_result = self.ants_private_share(pid,'mediaId',result,'mediaId',pid)
            if share_result ==-1 or share_result ==-100:
                self.write_str(u"1.0.3-2.3 视频发布之后，个人分享列表访问异常 error")
                self.write_email_log(u"1.0.3-2.3"," 视频发布之后，个人分享列表访问异常",'error')
            elif len(share_result)>1:
                self.write_str(u"1.0.3-2.3 视频发布之后，个人分享列表数据重复 fail")
                self.write_email_log(u"1.0.3-2.3"," 视频发布之后，个人分享列表数据重复",'fail')
            else:
                self.write_str(u"1.0.3-2.3 视频发布之后，个人分享列表数据展示 success")
                self.write_email_log(u"1.0.3-2.3"," 视频发布之后，个人分享列表数据展示",'success')

            # 个人信息列表
            userInfo = self.ants_get_user_info(pid,'shares',pid)
            print(userInfo)
            userInfo_time2=self.get_now_time()
            if userInfo==-1 or userInfo == -100:
                self.write_str("1.0.3-2.4 发布媒体之后,个人信息列表出现异常了")
                self.write_email_log("1.0.3-2.4"," 发布媒体之后,个人信息列表出现异常了","error")
            elif userInfo== (userInfo_result_end+1):
                self.write_str(u"1.0.3-2.4 发布媒体之后,发布影响个人信息列表 success,耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.3-2.4"," 发布媒体之后,发布影响个人信息列表,耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.3-2.4 发布媒体之后,发布影响个人信息列表 fail")
                self.write_email_log(u"1.0.3-2.4"," 发布媒体之后,发布影响个人信息列表","fail")

            # 发布影响首页列表==========1.0.1——1.2===================
            index_time1 =self.get_now_time()
            index_result = self.ants_index('mediaId',result,'mediaId',pid)
            print(index_result)
            index_time2=self.get_now_time()
            if len(index_result)>1:
                self.write_str('1.0.3-2.5 发布媒体之后,首页列表数据重复 error')
                self.write_email_log('1.0.3-2.5',' 发布媒体之后,首页列表数据重复','error')
            elif index_result[0]==result:
                self.write_str(u"1.0.3-2.5 发布媒体之后,发布人查看首页列表存在且唯一 success,耗时"+str(self.get_time_long(index_time1,index_time2)))
                self.write_email_log(u"1.0.3-2.5"," 发布媒体之后,发布人查看首页列表存在且唯一,耗时"+str(self.get_time_long(index_time1,index_time2)),"success")
            
                #判断是否重复
                mediaUrls_index= self.ants_index('mediaId',result,'mediaUrl',pid)  
                mediaIds_index= self.ants_index('mediaUrl',mediaUrls_index[0],'mediaId',pid) 
                print(mediaIds_index)

                if mediaIds_index ==-1 or mediaIds_index ==-100:
                    self.write_str('1.0.3-2.6 首页发布之后，首页访问异常')
                    self.write_email_log('1.0.3-2.6',' 首页发布之后，首页访问异常','error')
                elif len(mediaIds_index)>1:
                    self.write_str('1.0.3-2.6 发布媒体之后,首页列表视频重复 error')
                    self.write_email_log('1.0.3-2.6',' 发布媒体之后,首页列表视频重复','error')
                else:
                    self.write_str('1.0.3-2.6 发布媒体之后,首页列表视频唯一 success')
                    self.write_email_log('1.0.3-2.6',' 发布媒体之后,首页列表视频唯一','success')
            else:
                self.write_str(u"1.0.3-2.5 发布媒体之后,发布影响媒体发布人查看首页列表 fail")
                self.write_email_log(u"1.0.3-2.5 ","发布媒体之后,发布影响媒体发布人查看首页列表","fail")

        # # 结束测试
        self.close_fd()
        self.EndTest()

        

def main():
    reload(sys)

    server,persons,serve_yy,server_firmware = inifile.get_input_params()
    cases = PubDel(server,serve_yy,"three")
    cases.run_cases(persons)


if __name__=="__main__":
    main()