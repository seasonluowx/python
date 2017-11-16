# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/2/22
import sys
from importlib import reload

from Common import Common

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# print(crupath
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)

import inifile


class commentByExcel(Common):
	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)
		# self.fdm = open(os.path.join(crupath,'result.txt'),'w')

	def runCase(self,persons):
		con_len=self.get_xls('testCase.xlsx','comment')
		for x in range(1,len(con_len)):
			param={}
			param['caseId'] =con_len[x][0]
			param['caseName'] =con_len[x][1]

			mediaId=con_len[x][2]
			if mediaId != '':
				param['mediaId']=int(mediaId)
			else:
				param['mediaId']=mediaId

			param['content']=con_len[x][3]
			userId=con_len[x][4]
			if userId != '':
				param['userId']=int(userId)
			else:
				param['userId']=userId

			add_result = self.ants_addComByExcel(param,persons[1])
			print(add_result)

			if add_result ==-1 or add_result == -100:
				self.write_str(str(param['caseId'])+str(param['caseName'])+"异常 error")
				self.write_email_log(str(param['caseId']),str(param['caseName'])+"异常","error")
				
			elif param['caseId']=='COMMENT_003' or param['caseId']=='COMMENT_004':
				if add_result['code'] == -500101:
					self.write_str(str(param['caseId'])+str(param['caseName'])+" success")
					self.write_email_log(str(param['caseId']),str(param['caseName']),"success")
				else:
					self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
					self.write_email_log(str(param['caseId']),str(param['caseName']),"fail")
		
			elif add_result['message'] == 'success':
				comresult = self.get_items(add_result,'result')
				print(comresult)
				if comresult['replyTo'] ==-1:
					comresult['replyTo'] =''

				if comresult['mediaId'] == param['mediaId'] and comresult['content'] == param['content'] and comresult['replyTo'] == param['userId']:
					self.write_str(str(param['caseId'])+str(param['caseName'])+" success")
					self.write_email_log(str(param['caseId']),str(param['caseName']),"success")
				else:
					self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
					self.write_email_log(str(param['caseId']),str(param['caseName']),"fail")
			else:
				self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
				self.write_email_log(str(param['caseId']),str(param['caseName']),"fail")

        



def main():
	reload(sys)

	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=commentByExcel(server,serve_yy,'twelve')
	case.runCase(persons)

if __name__ == '__main__':
	main()