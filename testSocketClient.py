import time,socket

def receive(sock):
	buffer=[]
	while True:
		d = sock.recv(1024)
		if d:
			buffer.append(d)
		else:
			break
	return ''.join(buffer)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('127.0.0.1', 9999))
print s.recv(1024)
for data in ['Michael', 'Tracy', 'Sarah']:
	s.send(data)
	print receive(s)
	# print(s.recv(1024))
s.send('exit')
s.close()