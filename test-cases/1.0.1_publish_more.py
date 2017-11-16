# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/2/14
# ----------------------

import os
import sys
from importlib import reload

from publish import Publish

crupath = sys.path[0] # [sys.path[0].find(':')+1:]

# print(crupath
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)
import inifile
import time


class PublishMedia(Publish):

    def __init__(self,server,server_yy,ModuleName):
        # print('&&&&&&&&&&&&'
        Publish.__init__(self,server,server_yy,ModuleName)


    def run_case(self,persons):
        # print("run publish case"
        runCase = False
        isRunClub =False
        if True:
            # 发布影响个人信息列表===========1.0.1——1======================
            userInfo_init = self.ants_get_user_info(persons[0],'shares',persons[0])

            
        # #发布
        publish_time1 =self.get_now_time()
        # 发布的一系列流程
        # =================== 3 =========================
        # 获取发布中body下的file Id值, 二
        fileId,mediaUrl,thumbUrl = self.ants_get_media_fileId(2,persons[0])
        
        # 获取后台自定义的media tags ，三
        #tags=[{'id': 1034, 'name': 'test111'}, {'id': 114, 'name': '14'}]
        tags = self.ants_get_media_tags(persons[0])
        print(tags)

        # 获取加入的club ，四
        clubsId = self.ants_get_clubs(persons[0])
        #clubsId =[289]
        if len(clubsId) < 1:
            clubId=''
        else:
            clubId=clubsId[0]
            isRunClub =True
        print(clubId)

        publish_time3 =self.get_now_time()
        # 完成媒体上传,五
        media = 'final.mp4'
        thumb = 'mao.jpg'
        isUpLoad = self.ants_upload_local_video_work(mediaUrl,thumbUrl,thumb,thumb)
        
        result=''
        if isUpLoad:
            print(isUpLoad)
            publish_time4 =self.get_now_time()
            self.write_str(u"1.0.1-0 上传图片 success,耗时："+str(self.get_time_long(publish_time3,publish_time4)))
            self.write_email_log(u"1.0.1-0 上传图片耗时："+str(self.get_time_long(publish_time3,publish_time4)),'success')
            
            start=time.clock()
            while True:
                publish_tt1 =self.get_now_time()
                result = self.ants_publish_media(persons[0],tags,clubId,fileId)
                publish_tt2 =self.get_now_time()
                end=time.clock()
                self.write_str(u"1.0.1-1 发布媒体 mediaId："+str(result)+",耗时："+str(self.get_time_long(publish_tt1,publish_tt2)))
                self.write_email_log("1.0.1-1 发布媒体 mediaId："+str(result)+",耗时："+str(self.get_time_long(publish_tt1,publish_tt2)),'success')
                # time.sleep(10)
                print(result)
                if result !=0:
                    mediaId=result
                    runCase=True
                    self.fdm.write(str(result))
                if int(end-start) > 10*60:
                    publish_tt3 =self.get_now_time()
                    result2 = self.ants_publish_media(persons[0],tags,clubId,fileId)
                    publish_tt4 =self.get_now_time()
                    end=time.clock()
                    self.write_str(u"1.0.1-1 发布媒体 mediaId："+str(result2)+",耗时："+str(self.get_time_long(publish_tt3,publish_tt4)))
                    self.write_email_log("1.0.1-1 发布媒体 mediaId："+str(result2)+",耗时："+str(self.get_time_long(publish_tt3,publish_tt4)),'success')
                    # self.fdm.write(str(result2))
                    self.fdm.close()
                    break     
        else:
            self.write_str(u"1.0.1-0 上传视频 fail")
            self.write_email_log(u"1.0.1-0 上传视频",'fail')

        if runCase:   
        # 发布影响媒体详情==========1.0.1——1.1 ===================
            detail_time1 = self.get_now_time();
            mediaInfoResult = self.ants_media_detail(mediaId,persons[0])
            detail_time2 = self.get_now_time();         
            mediaStatus=self.isStatus(mediaInfoResult)
            # print(str(mediaInfoResult)
            if mediaStatus:
                self.write_str(u"1.0.1-1.1 发布影响媒体详情 success,耗时"+str(self.get_time_long(detail_time1,detail_time2)))
                self.write_email_log(u"1.0.1-1.1 发布影响媒体详情","success")
            else:
                self.write_str(u"1.0.1-1.1 发布影响媒体详情 fail")
                self.write_email_log(u"1.0.1-1.1 发布影响媒体详情,耗时"+str(self.get_time_long(detail_time1,detail_time2)),"fail")

        # 发布影响首页列表==========1.0.1——1.2=======byKey,byKeyValue,key_word,pid============
            index_time1 =self.get_now_time()
            index_result = self.ants_index('mediaId',mediaId,'mediaId',persons[0])
            if len(index_result)>1:
                self.write_str(u"1.0.1-1.2 发布媒体之后,首页列表有重复 fail")
                self.write_email_log(u"1.0.1-1.2发布媒体之后,首页列表有重复","fail")
            else:
                index_time2=self.get_now_time()
                if index_result[0]==mediaId:
                    self.write_str(u"1.0.1-1.2 发布媒体之后,发布影响媒体发布人查看首页列表 success,耗时"+str(self.get_time_long(index_time1,index_time2)))
                    self.write_email_log(u"1.0.1-1.2 发布媒体之后,发布影响媒体发布人查看首页列表,耗时"+str(self.get_time_long(index_time1,index_time2)),"success")
                
                    index_time1 =self.get_now_time()
                    index_mediaUrl = self.ants_index('mediaId',mediaId,'mediaUrl',persons[0])
                    print(index_mediaUrl)
                    if len(index_result)<1:
                        self.write_str(u"1.0.1-1.3 发布媒体之后, 首页加载图片数据 fail")
                        self.write_email_log(u"1.0.1-1.3发布媒体之后,首页加载图片数据","fail")
                    else:
                        index_time2=self.get_now_time() 
                        mediaUrl_result3 = self.ants_index('mediaUrl',index_mediaUrl[0],'mediaId',persons[0])
                        print(str(mediaUrl_result3)+'****')
                        if len(mediaUrl_result3)>1:
                            self.write_str(u"1.0.1-1.4 发布媒体之后,媒体重复发布，id为"+str(mediaUrl_result3)+",耗时"+str(self.get_time_long(index_time1,index_time2)))
                            self.write_email_log(u"1.0.1-1.4 发布媒体之后,媒体重复发布，id为"+str(mediaUrl_result3)+",耗时"+str(self.get_time_long(index_time1,index_time2)),"success")
                        else:
                            self.write_str(u"1.0.1-1.4 发布媒体之后,首页上传图片唯一 success")
                            self.write_email_log(u"1.0.1-1.4发布媒体之后,首页上传图片唯一 ","success")

                else:
                    self.write_str(u"1.0.1-1.2 发布媒体之后,发布影响媒体发布人查看首页列表 fail")
                    self.write_email_log(u"1.0.1-1.2发布媒体之后,发布影响媒体发布人查看首页列表","fail")
            

        # 发布影响好友查看首页列表==========1.0.1——1.3===================
            isFollowListEnd = self.ants_isFollows(persons[0],1,persons[1])
            print(isFollowListEnd)
            if isFollowListEnd == False:
                #添加关注
                self.ants_follow(persons[0],1,persons[1])
            
            #好友同步，可能时间较长，设置2min等待
            # time.sleep(120)   
            index_time3=self.get_now_time()
            index_result_hy = self.ants_index('mediaId',mediaId,'mediaId',persons[1])
            
            index_time4=self.get_now_time()
            if index_result_hy[0]==mediaId:
                self.write_str(u"1.0.1-1.5 发布媒体之后,发布影响好友查看首页列表 success,耗时"+str(self.get_time_long(index_time3,index_time4)))
                self.write_email_log(u"1.0.1-1.5 发布媒体之后,发布影响好友查看首页列表,耗时"+str(self.get_time_long(index_time3,index_time4)),"success")
            else:
                self.write_str(u"1.0.1-1.5 发布媒体之后,发布影响好友查看首页列表 fail")
                self.write_email_log(u"1.0.1-1.5发布媒体之后,发布影响好友查看首页列表","fail")

        # 发布不影响非好友用户查看首页==========1.0.1——1.4===================   
            isFollowListEnd = self.ants_isFollows(persons[0],1,persons[2])
            print(isFollowListEnd)
            if isFollowListEnd == True:
                #取消关注
                self.ants_follow(persons[0],0,persons[2])
            index_time5=self.get_now_time()
            follow_mediaId_result = self.ants_index('mediaId',mediaId,'mediaId',persons[2])
            print(index_result_hy)
            print('======')
            index_time6=self.get_now_time()
            if follow_mediaId_result==-1:
                self.write_str(u"1.0.1-1.6 发布媒体之后,发布不影响非好友用户查看首页 success,耗时"+str(self.get_time_long(index_time5,index_time6)))
                self.write_email_log(u"1.0.1-1.6 发布媒体之后,发布不影响非好友用户查看首页,耗时"+str(self.get_time_long(index_time5,index_time6)),"success")
            else:
                self.write_str(u"1.0.1-1.6 发布媒体之后,发布不影响非好友用户查看首页 fail")
                self.write_email_log(u"1.0.1-1.6发布媒体之后,发布不影响非好友用户查看首页","fail")

        # 发布影响标签最新列表-发布人==========1.0.1——1.6===================    
            for x in range(len(tags)):
                mediaIndex_time1=self.get_now_time()
                tagId=tags[x]['id']
                tag_mediaId_result = self.ants_tags_least(tagId,'mediaId',mediaId,'mediaId',persons[0])
                mediaIndex_time2=self.get_now_time()
                if len(tag_mediaId_result)>0 and tag_mediaId_result[0]==mediaId:
                    self.write_str(u"1.0.1-1.7 发布媒体之后,发布影响标签"+tags[x]['name']+"最新列表 success,耗时"+str(self.get_time_long(mediaIndex_time1,mediaIndex_time2)))
                    self.write_email_log(u"1.0.1-1.7 发布媒体之后,发布影响标签"+tags[x]['name']+"最新列表,耗时"+str(self.get_time_long(mediaIndex_time1,mediaIndex_time2)),"success")
                    
                    #判断重复
                    tag_mediaUrl_result = self.ants_tags_least(tagId,'mediaId',mediaId,'mediaUrl',persons[0])
                    tagListPics = self.ants_tags_least(tagId,'mediaUrl',tag_mediaUrl_result[0],'mediaId',persons[0])
                    print(tagListPics)
                    if len(tagListPics)>1 :
                        self.write_str(u"1.0.1-1.8 发布媒体之后,标签最新列表"+tags[x]['name']+"重复展示，id为"+str(tagListPics)+",耗时"+str(self.get_time_long(index_time1,index_time2)))
                        self.write_email_log(u"1.0.1-1.8 发布媒体之后,标签最新列表"+tags[x]['name']+"重复展示，id为"+str(tagListPics)+",耗时"+str(self.get_time_long(index_time1,index_time2)),"success")
                    else:
                        self.write_str(u"1.0.1-1.8 发布媒体之后,标签最新列表"+tags[x]['name']+"上传图片唯一 success")
                        self.write_email_log(u"1.0.1-1.8发布媒体之后,标签最新列表"+tags[x]['name']+"上传图片唯一 ","success")

                else:
                    self.write_str(u"1.0.1-1.7 发布媒体之后,发布影响标签"+tags[x]['name']+"最新列表 fail")
                    self.write_email_log(u"1.0.1-1.7发布媒体之后,发布影响标签"+tags[x]['name']+"最新列表","fail")

        # 发布影响个人分享列表======1.0.1——1.6======
            shares_time1 =self.get_now_time()
            share_result = self.ants_private_share(persons[0],'mediaId',mediaId,'mediaId',persons[0])
            shares_time2=self.get_now_time()
            # print(share_result
            if len(share_result)>0 and share_result[0] ==mediaId:
                self.write_str(u"1.0.1—1.9 发布媒体之后,发布影响人分享列表 success,耗时"+str(self.get_time_long(shares_time1,shares_time2)))
                self.write_email_log(u"1.0.1—1.9 发布媒体之后,发布影响人分享列表,耗时"+str(self.get_time_long(shares_time1,shares_time2)),"success")

                #判断重复
                private_mediaUrl = self.ants_private_share(persons[0],'mediaId',mediaId,'mediaUrl',persons[0])
                private_mediaIds = self.ants_private_share(persons[0],'mediaUrl',private_mediaUrl[0],'mediaId',persons[0])
                if len(private_mediaIds)>1:
                    self.write_str(u"1.0.1-1.10 发布媒体之后,个人分享列表重复展示，id为"+str(private_mediaIds))
                    self.write_email_log(u"1.0.1-1.10 发布媒体之后,个人分享列表重复展示，id为"+str(private_mediaIds),"success")
                else:
                    self.write_str(u"1.0.1-1.10 发布媒体之后,个人分享列表上传图片唯一 success")
                    self.write_email_log(u"1.0.1-1.10发布媒体之后,个人分享列表上传图片唯一 ","success")
            else:
                self.write_str(u"1.0.1—1.9 发布媒体之后,发布影响人分享列表 fail")
                self.write_email_log(u"1.0.1—1.9 发布媒体之后,发布影响人分享列表","fail")  
        
        # 发布影响个人信息列表==========1.0.1——1.7===================
            userInfo_time1=self.get_now_time()
            userInfo = self.ants_get_user_info(persons[0],'shares',persons[0])
            userInfo_time2=self.get_now_time()
            # print(userInfo
            if userInfo_init== (userInfo-2):
                self.write_str(u"1.0.1-1.11 发布媒体之后,发布影响个人信息列表 success,耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)))
                self.write_email_log(u"1.0.1-1.11 发布媒体之后,发布影响个人信息列表,耗时"+str(self.get_time_long(userInfo_time1,userInfo_time2)),"success")
            else:
                self.write_str(u"1.0.1-1.11 发布媒体之后,发布影响个人信息列表 fail")
                self.write_email_log(u"1.0.1-1.11 发布媒体之后,发布影响个人信息列表","fail") 

        # #发布影响俱乐部最新列表==========1.0.1——1.9===================
        #     if isRunClub:
        #         city_time1=self.get_now_time()
        #         result_club_least = self.ants_club_latest(clubId,'mediaId',mediaId,'mediaId',persons[0])
        #         print(result_club_least
        #         city_time2=self.get_now_time()
        #         # print(userInfo
        #         if len(result_club_least)>0 and result_club_least[0]== mediaId:
        #             self.write_str(u"1.0.1-1.9 发布媒体之后,发布影响俱乐部最新列表 success,耗时"+str(self.get_time_long(city_time1,city_time2)))
        #             self.write_email_log(u"1.0.1-1.9 发布媒体之后,发布影响俱乐部最新列表,耗时"+str(self.get_time_long(city_time1,city_time2)),"success")
        #         else:
        #             self.write_str(u"1.0.1-1.9 发布媒体之后,发布影响俱乐部最新列表 fail")
        #             self.write_email_log(u"1.0.1-1.9 发布媒体之后,发布影响俱乐部最新列表","fail")
        # 结束测试
        self.close_fd()
        self.EndTest()

    #获取发布标签
    def ants_get_media_tags(self,person):
        method = 'GET'
        url = self.server+'/tags?v=v3.2'
        tags = self.get_media_tags(method,url,person)
        # self.write_str(str(tags)+'======')
        return tags

    #获取我加入的club
    def ants_get_clubs(self,person):
        ax=[]
        method = 'GET'
        url = self.server+'/clubs?v=v3.2'
        clubs = self.get_clubs(method,url,person)
        # self.write_str(str(clubs)+'======')
        for x in range(len(clubs)):
            if clubs[x]['status'] ==0:
                clubId = clubs[x]['clubId']
                ax.append(clubId)
        # print(str(ax)+'****'
        # return str(ax).strip('[').strip(']')
        return ax

    # #媒体发布
    # def ants_publish_media(self,person,tags,clubId,fileId):
    #     method = 'POST'
    #     bodys = {}
    #     bodys['tags'] = tags
    #     bodys['clubId'] = clubId
    #     bodys['fileId'] = fileId
    #     bodys['width'] = 1000
    #     bodys['height'] = 1000
    #     bodys['length'] = 10
    #     bodys['mediaType'] = 2
    #     bodys['mediaMemo'] = 'publish --fzh--- test'
    #     bodys['exIf'] = 'id 3'
    #     bodys['latitude'] = 31.55
    #     bodys['longitude'] = 121.25 
    #     bodys['locationDesc'] = '上海浦东新区，长泰广场'
    #     url = self.server+'/media?v=v3.2'
    #     result = self.publish(method,url,bodys,person)
    #     # print(type(result)
    #     self.write_str("fzh_mediaId number " + str(result))
    #     if isinstance(result,int):
    #         return result
    #     return 0
    
    # # 发布媒体
    # def publish(self,method,url,bodys,person,server):
    #     try:
    #         ax = []
    #         ax.append('result')
    #         status = self.post_general_fuc(method,url,bodys,'result',ax,person,server)
    #         return status
    #     except Exception as e:
    #         traceback.print_exc()


def main():

    reload(sys)


    server,persons,serve_yy,server_firmware = inifile.get_input_params()

    case = PublishMedia(server,serve_yy,"ten")
    case.run_case(persons)


if __name__=="__main__":
    main()