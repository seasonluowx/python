# coding: UTF-8
# ----------------------
# Author : fzh
# Time : 2017/2/22
import json
import sys
import time
from importlib import reload

from Common import Common

crupath = sys.path[0] # [sys.path[0].find(':')+1:]
# print(crupath
# scriptpath = os.path.join(crupath,'common')
# sys.path.append(scriptpath)


import inifile


class publishByExcel(Common):
	def __init__(self,server,serve_yy,moduleName):
		Common.__init__(self,server,serve_yy,moduleName)
		# self.fdm = open(os.path.join(crupath,'result.txt'),'w')

	def runCase(self,persons):
		con_len=self.get_xls('testCase.xlsx','publish')
		for x in range(1,len(con_len)):
			param={}
			param['caseId'] =con_len[x][0]
			param['caseName'] =con_len[x][1]
			param['width'] =int(con_len[x][2])
			param['height']=int(con_len[x][3])
			param['length']=int(con_len[x][4])

			mediaType=con_len[x][5]
			if mediaType != 'NULL' and mediaType !='':
				param['mediaType']=int(mediaType)
			else:
				param['mediaType']=mediaType

			param['mediaMemo']=con_len[x][6]
			param['fileId'] = con_len[x][7]

			shareChannel=con_len[x][8]
			if shareChannel !='NULL' and shareChannel !='':
				param['shareChannel']=int(shareChannel)
			else:
				param['shareChannel']=shareChannel
			param['tags']=con_len[x][9]
			size=con_len[x][10]
			if size !='NULL' and size !='':
				param['size']=int(size)
			
			param['exIf']=con_len[x][11]
			param['latitude']=con_len[x][12]
			param['longitude']=con_len[x][13]
			param['locationDesc']=con_len[x][14]

			self.publishMedia(param,persons)

	def publishMedia(self,param,persons):
		publish_time1 =self.get_now_time()
		# 获取发布中body下的file Id值, 二
		mediaType_ex=param['mediaType']
		

		
		if mediaType_ex =='' or mediaType_ex == 'NULL':
			fileId,mediaUrl,thumbUrl,uploadMethod = self.ants_get_media_fileId(2,persons[0])
		else:
			fileId,mediaUrl,thumbUrl,uploadMethod = self.ants_get_media_fileId(mediaType_ex,persons[0])

		
		if param['fileId'] ==1.0:
			param['fileId'] = fileId

		print(str(param['fileId'])+'----------')
		
		if mediaUrl != '':
			# 完成媒体上传,五
			media = 'mao.jpg'
			thumb = 'mao.jpg'            
			result=''
			for x in range(1,5):
				publish_time3 =self.get_now_time()
				isUpLoad = self.ants_upload_local_video_work(mediaUrl,media,thumbUrl,thumb)
				publish_time4 =self.get_now_time()
				if isUpLoad ==True:
					print(isUpLoad)
					self.write_str(str(param['caseId'])+"第"+str(x)+"次上传视频 success,耗时："+str(self.get_time_long(publish_time3,publish_time4)))
					self.write_email_log(str(param['caseId']),"第"+str(x)+"次上传视频耗时："+str(self.get_time_long(publish_time3,publish_time4)),'success')

					print(str(param))
					result = self.ants_publish_media(param,'v3.2',persons[0])
					publish_time2 =self.get_now_time()
					print(result)
    
					if param['caseId'] =='PUBLISH_005' or param['caseId'] =='PUBLISH_006':
						if result['code'] ==-500101:
							self.write_str(str(param['caseId'])+str(param['caseName'])+" success,耗时："+str(self.get_time_long(publish_time1,publish_time2)))
							self.write_email_log(str(param['caseId']),str(param['caseName'])+",耗时："+str(self.get_time_long(publish_time1,publish_time2)),'success')
						else:
							self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
							self.write_email_log(str(param['caseId']),str(param['caseName']),'fail')
					elif param['caseId'] =='PUBLISH_007':
						if result['code'] ==-500201:
							self.write_str(str(param['caseId'])+str(param['caseName'])+" success,耗时："+str(self.get_time_long(publish_time1,publish_time2)))
							self.write_email_log(str(param['caseId']),str(param['caseName'])+",耗时："+str(self.get_time_long(publish_time1,publish_time2)),'success')
						else:
							self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
							self.write_email_log(str(param['caseId']),str(param['caseName']),'fail')
					elif param['caseId'] =='PUBLISH_008':
						if result['code'] ==-500200:
							self.write_str(str(param['caseId'])+str(param['caseName'])+" success,耗时："+str(self.get_time_long(publish_time1,publish_time2)))
							self.write_email_log(str(param['caseId']),str(param['caseName'])+",耗时："+str(self.get_time_long(publish_time1,publish_time2)),'success')
						else:
							self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
							self.write_email_log(str(param['caseId']),str(param['caseName']),'fail')
					elif str(result).isdigit() == True and result !=0:
						self.write_str(str(param['caseId'])+str(param['caseName'])+str(result)+" success,耗时："+str(self.get_time_long(publish_time1,publish_time2)))
						self.write_email_log(str(param['caseId']),str(param['caseName'])+str(result)+",耗时："+str(self.get_time_long(publish_time1,publish_time2)),'success')
						
						#媒体详情
						detail=self.ants_media_detail(result,persons[0])
						if detail ==-1 or detail ==-100:
							self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情展示异常')
							self.write_email_log(str(param['caseId'])+str(param['caseName'])+'后媒体详情展示异常','error')
						else:
							print(detail)
							tag2 = detail[0]['tagList']
							width2 = detail[0]['width']
							height2 = detail[0]['height']
							length2 = detail[0]['length']
							mediaType2 = detail[0]['mediaType'] 
							mediaMemo2 = detail[0]['mediaMemo']
							latitude2 = detail[0]['latitude']
							longitude2 = detail[0]['longitude']
							locationDesc2 = detail[0]['locationDesc']

							tag=param['tags']
							print(str(len(tag))+'======'+str(tag)+'------'+str(tag2)+'==='+str(width2))

							tagsExcel=[]
							tagNameDetail=[]

							if tag !='' and tag !=[]:
								tagIds=json.loads(tag)
								for x in tagIds:
									tagName= x['name']
									tagsExcel.append(str(tagName))

							for y in range(len(tag2)):
								detailName=tag2[y]['name']
								tagNameDetail.append(detailName)
									
					
							if tagsExcel == tagNameDetail:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情tag:'+str(tagNameDetail)+' success')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情tag: '+str(tagNameDetail),'success')
							else:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情tag:'+str(tagNameDetail)+' fail')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情tag:'+str(tagNameDetail),' fail')
							
							if width2 == param['width']:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情width:'+str(width2)+' success')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情width: '+str(width2),'success')
							else:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情width:'+str(width2)+' fail')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情width:'+str(width2),' fail')

							if mediaMemo2 == param['mediaMemo']:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情mediaMemo:'+str(mediaMemo2)+' success')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情mediaMemo: '+str(mediaMemo2),'success')
							else:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情mediaMemo:'+str(mediaMemo2)+' fail')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情mediaMemo:'+str(mediaMemo2),' fail')
							
							if latitude2 == param['latitude'] or (latitude2==0 and param['latitude'] ==''):
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情latitude:'+str(latitude2)+' success')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情latitude: '+str(latitude2),'success')
							else:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情latitude:'+str(latitude2)+' fail')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情latitude:'+str(latitude2),' fail')

							if longitude2 == param['longitude'] or (longitude2==0 and param['longitude'] ==''):
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情longitude:'+str(longitude2)+' success')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情longitude: '+str(longitude2),'success')
							else:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情longitude:'+str(longitude2)+' fail')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情longitude:'+str(longitude2),' fail')

							if locationDesc2 == param['locationDesc']:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情latitude:'+str(locationDesc2)+' success')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情latitude: '+str(locationDesc2),'success')
							else:
								self.write_str(str(param['caseId'])+str(param['caseName'])+'后媒体详情latitude:'+str(locationDesc2)+' fail')
								self.write_email_log(str(param['caseId']),str(param['caseName'])+'后媒体详情latitude:'+str(locationDesc2),' fail')
						
						#删除媒体
						del_time1 =self.get_now_time()
						deleteMedia_result = self.ants_delete_media(result,persons[0])
						del_time2=self.get_now_time()
						print(deleteMedia_result)
						if deleteMedia_result =='success':
							self.write_str(str(param['caseId'])+str(param['caseName'])+'后删除媒体'+str(result)+'success，耗时'+str(self.get_time_long(del_time1,del_time2)))
							self.write_email_log(str(param['caseId']),str(param['caseName'])+'后删除媒体'+str(result)+'success，耗时'+str(self.get_time_long(del_time1,del_time2)),'success')
						else:
							self.write_str(str(param['caseId'])+str(param['caseName'])+'后删除媒体'+str(result)+'fail')
							self.write_email_log(str(param['caseId']),str(param['caseName'])+'后删除媒体'+str(result),'fail')

						#媒体详情
						detail_end=self.ants_media_detail(result,persons[0])
						print(detail_end)
						if detail_end==-1 or detail_end ==-100:
							self.write_str(str(param['caseId'])+str(param['caseName'])+'删除媒体后媒体详情展示异常')
							self.write_email_log(str(param['caseId']),str(param['caseName'])+'删除媒体后媒体详情展示异常','error')
						elif detail_end['code']==-500313:
							self.write_str(str(param['caseId'])+str(param['caseName'])+'删除媒体后媒体详情展示 success')
							self.write_email_log(str(param['caseId']),str(param['caseName'])+'删除媒体后媒体详情展示','success')
						else:
							self.write_str(str(param['caseId'])+str(param['caseName'])+'删除媒体后媒体详情展示 fail ')
							self.write_email_log(str(param['caseId']),str(param['caseName'])+'删除媒体后媒体详情展示','fail')

						time.sleep(5)
					else:
						self.write_str(str(param['caseId'])+str(param['caseName'])+" fail")
						self.write_email_log(str(param['caseId']),str(param['caseName']),'fail')
					break
				else:
					self.write_str(str(param['caseId'])+"第"+str(x)+"次上传视频 fail")
					self.write_email_log(str(param['caseId']),"第"+str(x)+"次上传视频",'fail')
					continue
                     
		else:
			self.write_str(str(param['caseId'])+"获取媒体发布url fail")
			self.write_email_log(str(param['caseId']),"获取媒体发布url",'fail')

        



def main():
	reload(sys)

	server,persons,serve_yy,server_firmware = inifile.get_input_params()

	case=publishByExcel(server,serve_yy,'eleven')
	case.runCase(persons)

if __name__ == '__main__':
	main()