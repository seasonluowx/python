import os
import sys

from resources import testconfig
from util import fileUtil
from cases import userInfo

crupath = sys.path[0]
import time


class PublishMedia():
    def __init__(self):
        self.server_sns=testconfig.configs['server_sns']
        self.ModuleName = "one"

    def runCase(self):
        persons = testconfig.configs["persons"]
        run_case = False
        isRunTag = False
        isRunClub = False
        pixelLevel = 0

        userId = fileUtil.get_pid()
        if userId == 'userId login fail!':
            pid = persons[0]
            self.fdm = open(os.path.join(crupath, 'userId.txt'), 'w')
            self.fdm.write(str(pid))
            self.fdm.close()
        else:
            pid = int(userId)

        if True:
            # 发布影响个人信息列表===========1.0.1——1======================
            userInfo_shares = userInfo.ants_get_user_info(pid, 'shares')

            # 发布影响我关注的人发布的媒体列表
            isFollowListEnd = self.ants_fllowList(pid, 1, persons[1])
            print(isFollowListEnd)
            if isFollowListEnd == False:
                # 添加关注
                self.ants_follow(pid, 1, persons[1])

            newShare_init = self.ants_media_followNewShare('result', persons[1])
            print('newShare_init:' + str(newShare_init))

            mediaId, tags, clubId, pixelLevel = self.publish_media(pid)
            print(str(mediaId) + '====' + str(tags) + '=====' + str(clubId) + '======' + str(pixelLevel))

            time.sleep(2)

            if mediaId != '' and mediaId != 0:
                run_case = True
            if tags != '':
                isRunTag = True
            if clubId != '':
                isRunClub = True

        if run_case:
            # 发布影响媒体详情==========1.0.1——1.1 ===================
            detail_time1 = self.get_now_time();
            mediaInfoResult = self.ants_media_detail(mediaId, pid)
            print(mediaInfoResult)
            detail_time2 = self.get_now_time();
            # print(str(mediaInfoResult)
            if mediaInfoResult == -1 or mediaInfoResult == -100:
                self.write_str(u"1.0.1-1.1 发布后媒体详情异常 error")
                self.write_email_log('1.0.1-1.1', "发布后媒体详情异常,耗时" + str(self.get_time_long(detail_time1, detail_time2)),
                                     "error")
            elif mediaInfoResult[0]['status'] == 0:
                self.write_str(u"1.0.1-1.1 发布影响媒体" + str(mediaId) + " 详情,媒体大小为" + str(
                    mediaInfoResult[0]['size']) + "KB， success,耗时" + str(
                    self.get_time_long(detail_time1, detail_time2)))
                self.write_email_log('1.0.1-1.1', "发布影响媒体" + str(mediaId) + " 详情,媒体大小为" + str(
                    mediaInfoResult[0]['size']) + "KB，耗时" + str(self.get_time_long(detail_time1, detail_time2)),
                                     "success")

                print(mediaInfoResult[0]['pixelLevel'])
                print(pixelLevel)
                if mediaInfoResult[0]['pixelLevel'] == pixelLevel:
                    self.write_str('1.0.1-1.1-1 发布媒体之后,媒体详情内pixelLevel展示 success')
                    self.write_email_log('1.0.1-1.1-1', '发布媒体之后,媒体详情内pixelLevel展示', 'success')
                else:
                    self.write_str('1.0.1-1.1-1 发布媒体之后,媒体详情内pixelLevel展示 fail')
                    self.write_email_log('1.0.1-1.1-1', '发布媒体之后,媒体详情内pixelLevel展示', 'fail')

            else:
                self.write_str(u"1.0.1-1.1 发布影响媒体详情 fail")
                self.write_email_log('1.0.1-1.1', "发布影响媒体详情,耗时" + str(self.get_time_long(detail_time1, detail_time2)),
                                     "fail")

            # 发布影响首页列表==========1.0.1——1.2===================
            index_time1 = self.get_now_time()
            index_result = self.ants_index('mediaId', mediaId, 'mediaId', pid)
            print(index_result)
            index_time2 = self.get_now_time()
            if len(index_result) > 1:
                self.write_str('1.0.1-1.2 发布媒体之后,首页列表数据重复 error')
                self.write_email_log('1.0.1-1.2', '发布媒体之后,首页列表数据重复', 'error')
            elif index_result[0] == mediaId:
                self.write_str(
                    u"1.0.1-1.2 发布媒体之后,发布人查看首页列表存在且唯一 success,耗时" + str(self.get_time_long(index_time1, index_time2)))
                self.write_email_log('1.0.1-1.2',
                                     "发布媒体之后,发布人查看首页列表存在且唯一,耗时" + str(self.get_time_long(index_time1, index_time2)),
                                     "success")

                # 判断是否重复
                mediaUrls_index = self.ants_index('mediaId', mediaId, 'mediaUrl', pid)
                mediaIds_index = self.ants_index('mediaUrl', mediaUrls_index[0], 'mediaId', pid)
                print(mediaIds_index)

                if mediaIds_index == -1 or mediaIds_index == -100:
                    self.write_str('1.0.1-1.3 首页发布之后，首页访问异常')
                    self.write_email_log('1.0.1-1.3', '首页发布之后，首页访问异常', 'error')
                elif len(mediaIds_index) > 1:
                    self.write_str('1.0.1-1.3 发布媒体之后,首页列表图片重复 error')
                    self.write_email_log('1.0.1-1.3', '发布媒体之后,首页列表图片重复', 'error')
                else:
                    self.write_str('1.0.1-1.3 发布媒体之后,首页列表图片唯一 success')
                    self.write_email_log('1.0.1-1.3', '发布媒体之后,首页列表图片唯一', 'success')

            else:
                self.write_str(u"1.0.1-1.2 发布媒体之后,发布影响媒体发布人查看首页列表 fail")
                self.write_email_log('1.0.1-1.2', "发布媒体之后,发布影响媒体发布人查看首页列表", "fail")

            # 发布影响好友查看首页列表==========1.0.1——1.3===================
            index_time3 = self.get_now_time()
            index_result_hy = self.ants_index('mediaId', mediaId, 'mediaId', persons[1])
            print(index_result_hy)
            # print('======'
            index_time4 = self.get_now_time()
            if index_result_hy == -1 or index_result_hy == -100:
                self.write_str(u"1.0.1-1.4 发布媒体之后,好友查看首页列表出现异常了")
                self.write_email_log("1.0.1-1.4", "发布媒体之后,好友查看首页列表出现异常了", "error")
            elif index_result_hy == False:
                self.write_str(u"1.0.1-1.4 发布媒体之后,发布影响好友查看首页列表 fail")
                self.write_email_log("1.0.1-1.4", "发布媒体之后,发布影响好友查看首页列表", "fail")
            elif len(index_result_hy) > 0 and index_result_hy[0] == mediaId:
                self.write_str(
                    u"1.0.1-1.4 发布媒体之后,发布影响好友查看首页列表 success,耗时" + str(self.get_time_long(index_time3, index_time4)))
                self.write_email_log("1.0.1-1.4",
                                     "发布媒体之后,发布影响好友查看首页列表,耗时" + str(self.get_time_long(index_time3, index_time4)),
                                     "success")
            else:
                self.write_str(u"1.0.1-1.4 发布媒体之后,发布影响好友查看首页列表 fail")
                self.write_email_log("1.0.1-1.4", "发布媒体之后,发布影响好友查看首页列表", "fail")

            # 发布不影响非好友用户查看首页==========1.0.1——1.4===================
            isFollowListEnd = self.ants_fllowList(pid, 1, persons[2])
            print(isFollowListEnd)
            if isFollowListEnd != False and isFollowListEnd != -1 and isFollowListEnd != -100:
                # 取消关注
                self.ants_follow(pid, 0, persons[2])
                time.sleep(2)

            index_time5 = self.get_now_time()
            follow_mediaId_result = self.ants_index('mediaId', mediaId, 'mediaId', persons[2])
            print(follow_mediaId_result)
            # print('======'
            index_time6 = self.get_now_time()
            if follow_mediaId_result == -100:
                self.write_str(u"1.0.1-1.5 发布媒体之后,非好友用户查看首页出现异常了")
                self.write_email_log("1.0.1-1.5", '发布媒体之后,非好友用户查看首页出现异常了', 'error')
            elif follow_mediaId_result == False:
                self.write_str(
                    u"1.0.1-1.5 发布媒体之后,发布不影响非好友用户查看首页 success,耗时" + str(self.get_time_long(index_time5, index_time6)))
                self.write_email_log("1.0.1-1.5",
                                     "发布媒体之后,发布不影响非好友用户查看首页,耗时" + str(self.get_time_long(index_time5, index_time6)),
                                     "success")
            else:
                self.write_str(u"1.0.1-1.5 发布媒体之后,发布不影响非好友用户查看首页 fail")
                self.write_email_log("1.0.1-1.5", "发布媒体之后,发布不影响非好友用户查看首页", "fail")

            # 发布影响标签最新列表-发布人==========1.0.1——1.6===================
            if isRunTag:
                for x in range(len(tags)):
                    mediaIndex_time1 = self.get_now_time()
                    tagId = tags[x]['id']
                    tag_mediaId_result = self.ants_tags_least(tagId, 'mediaId', mediaId, 'mediaId', pid)
                    print(tag_mediaId_result)
                    # print('======'
                    mediaIndex_time2 = self.get_now_time()
                    if tag_mediaId_result == -1 or tag_mediaId_result == -100:
                        self.write_str("1.0.1-1.6 发布媒体之后,标签最新列表出现异常了 error")
                        self.write_email_log("1.0.1-1.6", "发布媒体之后,标签最新列表出现异常了", "error")
                    elif len(tag_mediaId_result) > 1:
                        self.write_str("1.0.1-1.6 发布媒体之后,标签最新列表数据重复 error")
                        self.write_email_log("1.0.1-1.6", "发布媒体之后,标签最新列表数据重复 error")
                    elif tag_mediaId_result[0] == mediaId:
                        self.write_str(u"1.0.1-1.6 发布媒体之后,标签" + tags[x]['name'] + "最新列表有且只有一条数据 success,耗时" + str(
                            self.get_time_long(mediaIndex_time1, mediaIndex_time2)))
                        self.write_email_log("1.0.1-1.6", "发布媒体之后,标签" + tags[x]['name'] + "最新列表有且只有一条数据,耗时" + str(
                            self.get_time_long(mediaIndex_time1, mediaIndex_time2)), "success")

                        # 判断重复
                        mediaUrls_tags = self.ants_tags_least(tagId, 'mediaId', mediaId, 'mediaUrl', pid)
                        mediaIds_tags = self.ants_tags_least(tagId, 'mediaUrl', mediaUrls_tags[0], 'mediaId', pid)
                        if mediaIds_tags == -1 or mediaIds_tags == -100:
                            self.write_str(u"1.0.1-1.7 发布媒体之后,标签最新列表出现异常了")
                            self.write_email_log("1.0.1-1.7", "发布媒体之后,标签最新列表出现异常了", "error")
                        elif len(mediaIds_tags) > 1:
                            self.write_str(u"1.0.1-1.7 发布媒体之后,标签最新列表图片重复展示")
                            self.write_email_log("1.0.1-1.7", "发布媒体之后,标签最新列表图片重复展示", "error")
                        else:
                            self.write_str(u"1.0.1-1.7 发布媒体之后,首页列表图片唯一")
                            self.write_email_log("1.0.1-1.7", "发布媒体之后,首页列表图片唯一", "success")
                    else:
                        self.write_str(u"1.0.1-1.6 发布媒体之后,发布影响标签" + tags[x]['name'] + "最新列表 fail")
                        self.write_email_log("1.0.1-1.6", "发布媒体之后,发布影响标签" + tags[x]['name'] + "最新列表", "fail")

                    # 发布影响标签用户列表
                    city_time1 = self.get_now_time()
                    tag_user = self.ants_tagUser(tagId, pid, pid)
                    print(tag_user)
                    city_time2 = self.get_now_time()
                    if tag_user == -1 or tag_user == -100:
                        self.write_str('1.0.1-1.13 发布媒体之后标签' + tags[x]['name'] + '用户列表异常 error')
                        self.write_email_log("1.0.1-1.13", "修发布媒体之后标签" + tags[x]['name'] + "用户列表异常", "error")
                    elif tag_user == False:
                        self.write_str('1.0.1-1.13 发布媒体之后影响标签' + tags[x]['name'] + '用户列表 fail')
                        self.write_email_log("1.0.1-1.13", "发布媒体之后影响标签" + tags[x]['name'] + "用户列表", "fail")
                    elif tag_user['userId'] == pid:
                        self.write_str('1.0.1-1.13 发布媒体之后影响标签' + tags[x]['name'] + '用户列表 success，耗时' + str(
                            self.get_time_long(city_time1, city_time2)))
                        self.write_email_log("1.0.1-1.13", " 发布媒体之后影响标签" + tags[x]['name'] + "用户列表，耗时" + str(
                            self.get_time_long(city_time1, city_time2)), "success")
                    else:
                        self.write_str('1.0.1-1.13 发布媒体之后影响标签' + tags[x]['name'] + '用户列表 fail')
                        self.write_email_log("1.0.1-1.13", "发布媒体之后影响标签" + tags[x]['name'] + "用户列表", "fail")

            # 发布影响个人分享列表======1.0.1——1.6======
            shares_time1 = self.get_now_time()
            share_result = self.ants_private_share(pid, 'mediaId', mediaId, 'mediaId', pid)
            print(share_result)
            # print('======'
            shares_time2 = self.get_now_time()
            if share_result == -1 or share_result == -100:
                self.write_str("1.0.1-1.8 发布媒体之后,个人分享列表出现异常了")
                self.write_email_log("1.0.1-1.8", "发布媒体之后,人分享列表出现异常了", "error")
            elif len(share_result) > 1:
                self.write_str("1.0.1-1.8 发布媒体之后,人分享列表数据重复 error")
                self.write_email_log("1.0.1-1.8", "发布媒体之后,人分享列表数据重复", "error")
            elif share_result[0] == mediaId:
                self.write_str(
                    u"1.0.1—1.8 发布媒体之后,个人分享列表有且只有一条记录 success,耗时" + str(self.get_time_long(shares_time1, shares_time2)))
                self.write_email_log("1.0.1-1.8",
                                     "发布媒体之后,个人分享列表有且只有一条记录,耗时" + str(self.get_time_long(shares_time1, shares_time2)),
                                     "success")

                # 判断重复
                mediaUrls_share = self.ants_private_share(pid, 'mediaId', mediaId, 'mediaUrl', pid)
                mediaIds_share = self.ants_private_share(pid, 'mediaUrl', mediaUrls_share[0], 'mediaId', pid)

                if mediaIds_share == -1 or mediaIds_share == -100:
                    self.write_str("1.0.1-1.9 发布媒体之后,个人分享列表出现异常了")
                    self.write_email_log("1.0.1-1.9", "发布媒体之后,个人分享列表出现异常了", "error")
                elif len(mediaIds_share) > 1:
                    self.write_str("1.0.1-1.9 发布媒体之后,人分享列表图片重复 error")
                    self.write_email_log("1.0.1-1.9", "发布媒体之后,人分享列表图片重复 error", "error")
                else:
                    self.write_str("1.0.1-1.9 发布媒体之后,人分享列表列表图片唯一")
                    self.write_email_log("1.0.1-1.9", "发布媒体之后,人分享列表列表图片唯一", "success")

            else:
                self.write_str(u"1.0.1—1.8 发布媒体之后,发布影响人分享列表 fail")
                self.write_email_log("1.0.1-1.9", "发布媒体之后,发布影响人分享列表", "fail")

                # 发布影响个人信息列表==========1.0.1——1.7===================
            userInfo_time1 = self.get_now_time()
            userInfo_shares_aft = self.ants_get_user_info(pid, 'shares', pid)
            print(userInfo_shares_aft)
            userInfo_time2 = self.get_now_time()
            if userInfo_shares_aft == -1 or userInfo_shares_aft == -100:
                self.write_str("1.0.1-1.10 发布媒体之后,个人信息列表出现异常了")
                self.write_email_log("1.0.1-1.10", "发布媒体之后,个人信息列表出现异常了", "error")
            elif userInfo_shares == (userInfo_shares_aft - 1):
                self.write_str(u"1.0.1-1.10 发布媒体之后,发布影响个人信息列表 success,耗时" + str(
                    self.get_time_long(userInfo_time1, userInfo_time2)))
                self.write_email_log("1.0.1-1.10",
                                     "发布媒体之后,发布影响个人信息列表,耗时" + str(self.get_time_long(userInfo_time1, userInfo_time2)),
                                     "success")
            else:
                self.write_str(u"1.0.1-1.10 发布媒体之后,发布影响个人信息列表 fail")
                self.write_email_log("1.0.1-1.10", "发布媒体之后,发布影响个人信息列表", "fail")

                # 发布影响俱乐部最新列表==========1.0.1——1.9===================
            if isRunClub:
                city_time1 = self.get_now_time()
                result_club_least = self.ants_club_latest(clubId, 'mediaId', mediaId, 'mediaId', pid)
                print(result_club_least)
                # print('======'
                city_time2 = self.get_now_time()
                # print(userInfo
                if result_club_least == -1 or result_club_least == -100:
                    self.write_str("1.0.1-1.11 发布媒体之后,俱乐部最新列表出现异常了")
                    self.write_email_log("1.0.1-1.11", "发布媒体之后,俱乐部最新列表出现异常了", "error")
                elif len(result_club_least) > 1:
                    self.write_str("1.0.1-1.11 发布媒体之后,俱乐部最新列表数据重复")
                    self.write_email_log("1.0.1-1.11", "发布媒体之后,俱乐部最新列表数据重复", "error")
                elif result_club_least[0] == mediaId:
                    self.write_str(u"1.0.1-1.11 发布媒体之后,俱乐部最新列表有且只有一条记录 success,耗时" + str(
                        self.get_time_long(city_time1, city_time2)))
                    self.write_email_log("1.0.1-1.11",
                                         "发布媒体之后,俱乐部最新列表有且只有一条记录,耗时" + str(self.get_time_long(city_time1, city_time2)),
                                         "success")

                    # 判断图片重复
                    mediaUrls_club = self.ants_club_latest(clubId, 'mediaId', mediaId, 'mediaUrl', pid)
                    mediaIds_club = self.ants_club_latest(clubId, 'mediaUrl', mediaUrls_club[0], 'mediaId', pid)
                    print(mediaIds_club)

                    if mediaIds_club == -1 or mediaIds_club == -100:
                        self.write_str("1.0.1-1.12 发布媒体之后,俱乐部最新列表出现异常了")
                        self.write_email_log("1.0.1-1.12", "发布媒体之后,俱乐部最新列表出现异常了", "error")
                    elif mediaIds_club == False:
                        self.write_str("1.0.1-1.11 发布媒体之后,俱乐部最新列表数据未更新 fail")
                        self.write_email_log("1.0.1-1.12", "发布媒体之后,俱乐部最新列表数据未更新", "fail")
                    elif len(mediaIds_club) > 1:
                        self.write_str("1.0.1-1.12 发布媒体之后,俱乐部最新列表图片重复")
                        self.write_email_log("1.0.1-1.12", "发布媒体之后,俱乐部最新列表图片重复", "error")
                    else:
                        self.write_str("1.0.1-1.12 发布媒体之后,俱乐部最新列表数据唯一")
                        self.write_email_log("1.0.1-1.12", "发布媒体之后,俱乐部最新列表数据唯一", "success")

                else:
                    self.write_str(u"1.0.1-1.11 发布媒体之后,发布影响俱乐部最新列表 fail")
                    self.write_email_log(u"1.0.1-1.11", "发布媒体之后,发布影响俱乐部最新列表", "fail")

            # 发布影响我关注的人发布的媒体列表==========1.0.1——1.7===================
            userInfo_time1 = self.get_now_time()
            newShare = self.ants_media_followNewShare('result', persons[1])
            print('发布媒体之前，result：' + str(newShare_init) + '发布媒体之后，result：' + str(newShare))
            userInfo_time2 = self.get_now_time()
            if newShare == -1 or newShare == -100:
                self.write_str("1.0.1-1.13 发布媒体之后,我关注的人发布的媒体列表出现异常了")
                self.write_email_log("1.0.1-1.13", "发布媒体之后,我关注的人发布的媒体列表出现异常了", "error")
            elif newShare == (newShare_init + 1):
                self.write_str(u"1.0.1-1.13 发布媒体之后,发布影响我关注的人发布的媒体列表 success,耗时" + str(
                    self.get_time_long(userInfo_time1, userInfo_time2)))
                self.write_email_log("1.0.1-1.13", "发布媒体之后,发布影响我关注的人发布的媒体列表,耗时" + str(
                    self.get_time_long(userInfo_time1, userInfo_time2)), "success")
            else:
                self.write_str(u"1.0.1-1.13 发布媒体之后,发布影响我关注的人发布的媒体列表 fail")
                self.write_email_log("1.0.1-1.13",
                                     "发布媒体之后,发布影响我关注的人发布的媒体列表,发布媒体之后，result：" + str(newShare) + "发布媒体之前，result：" + str(
                                         newShare_init), "fail")

                # 结束测试
        self.close_fd()
        self.EndTest()


def main():
    case = PublishMedia()
    case.runCase()


if __name__ == "__main__":
    main()
