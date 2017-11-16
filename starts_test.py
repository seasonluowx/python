import time
from cases.login import Login
from cases.publish import PublishMedia
# cases.append(os.path.join(testCasesPath,"1.0.2_comments.py"))
# cases.append(os.path.join(testCasesPath,"1.0.4_like.py"))
# cases.append(os.path.join(testCasesPath,"1.0.5_follow.py"))
# cases.append(os.path.join(testCasesPath,"1.0.6_userInfo.py"))
# cases.append(os.path.join(testCasesPath,"1.0.8_videoList.py"))
# cases.append(os.path.join(testCasesPath,"1.0.9_find.py"))
# cases.append(os.path.join(testCasesPath,"1.0.11_others.py"))
# cases.append(os.path.join(testCasesPath,"1.0.12_message.py"))
# cases.append(os.path.join(testCasesPath,"1.0.13_live.py"))
# cases.append(os.path.join(testCasesPath,"1.0.14_recom.py"))
# cases.append(os.path.join(testCasesPath,"1.0.15_screen.py"))
# cases.append(os.path.join(testCasesPath,"1.0.3_mediaDel.py"))
# cases.append(os.path.join(testCasesPath,"1.0.16_publishByExcel.py"))
# cases.append(os.path.join(testCasesPath,"1.0.17_commentByExcel.py"))
# cases.append(os.path.join(testCasesPath,"1.0.18_redLog.py"))
# cases.append(os.path.join(testCasesPath, "2.0.0_firmware_list.py"))


def Start():
    now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    # 记录开始时间
    with open('time.txt', 'w') as fdm:
        fdm.write(str(now_time))

    Login().runCase()
    PublishMedia().runCase()

if __name__ == "__main__":
    Start()
