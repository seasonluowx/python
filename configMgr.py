import configparser

config = configparser.ConfigParser();
config.read('common.ini',encoding='utf-8-sig')
name=config.get('base','name')
age=config.get('base','age')
comefrom=config.get('base','comefrom')
sex=config.get('base','sex')
print('你好,%s岁的来自%s的叫做%s的%s人'%(age,comefrom,name,sex))