import socket
i = 0
while i < 100:
	mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mysock.connect(('127.0.0.1', 12007))
	cmd = 'GET /form1.html HTTP/1.0\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		break
	print(data.decode(),end='')
	mysock.close()
	i+=1
print("--------------",i)
