from enum import Enum
# wight=77.3
# hight=1.77
# bmi=wight/hight/hight
# if bmi<18.5:
#	print('you are too light')
# elif bmi>=18.5 and bmi<25:
#	print('your wight is standand')
# elif bmi>=25 and bmi< 28:
#	print('you are weight')
# elif bmi>=28 and bmi<32:
#	print('your are fat')
# else:
#	print('you are too fat')
# sum=0
# for x in range(101):
#	sum=sum+x
# print(sum)
# list1=['jessy','merry','cherry']
# for name in list1:
#	print('hello;'+name)
list2=[1,3,5,7,9]
def product(x,y):
	return x*y
print(reduce(product,list2))
def is_palindrome(n):
	return str(n)==str(n)[::-1]
output = filter(is_palindrome, range(1, 1000))
print(list(output))
L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
def by_name(t):
	return t[0].lower
def by_sort(t):
	return t[1]
L2=sorted(L,key=by_name)
L3=sorted(L,key=by_sort,reverse=True)
print(L2)
print(L3)
print(0.45359*175)
f=lambda x,y:x*y
print(f(2,5))

class Screen(object):
	@property
	def width(self):
		return self._width
	@width.setter
	def width(self,value):
		self._width=value
	@property
	def height(self):
		return self._height
	@height.setter
	def height(self,value):
		self._height=value
	@property
	def resolution(self):
		return self._height*self._width
		
s = Screen()
s.width=2048
s.height=1080
print('%s,%s,%s',s.width,s.height,s.resolution)
print(type(s))

