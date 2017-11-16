# coding: UTF-8
# ----------------------
# Author : Jake
# Time : 2017/9/22
# ----------------------

import sys
from importlib import reload

import inifile
from Common import Common

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# print(crupath
# scriptpath = os.path.join(crupath,'common')
# print(scriptpath
# sys.path.append(scriptpath)


class Like(Common):

    def __init__(self,server,serve_yy,ModuleName):
        Common.__init__(self,server,serve_yy,ModuleName)

    def run_cases(self,persons,server_firmware):
        # print("run cases"

        sfirmware = server_firmware.strip().split(',')
        for i in range(len(sfirmware)):
            if i==0:
                name = 'CN'
            elif i==1:
                name = 'EN'
            firmwares = self.ants_firmware_list(persons[0],sfirmware[i])
            self.write_str(str(firmwares))
            self.write_email_log("2.0.0  ",name + " 固件更新列表："+str(len(firmwares)),"success")


        # # 结束测试
        self.close_fd()
        self.EndTest()



def main():
    reload(sys)

    
    server,persons,serve_yy,server_firmware = inifile.get_input_params()
    cases = Like(server,serve_yy,"firmwares")
    cases.run_cases(persons,server_firmware)


if __name__=="__main__":
    main()