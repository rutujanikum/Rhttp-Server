import socket
import threading
import _thread

mutex = _thread.allocate_lock()
i = 0
def singleGet(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'GET /form1.html HTTP/1.0\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()
	
def singlePost(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'POST /form1.html HTTP/1.0\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()

def getWithHeader(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'GET /form1.html HTTP/1.0\r\nUser-Agent: Client Program\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nConnection: keep-alive\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()
	
def postWithHeader(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'POST /del1.html HTTP/1.1\r\nContent-Type: text/html\r\nUser-Agent: PostmanRuntime/7.26.8\r\nAccept: */*\r\nPostman-Token:\r\na3135fe6-80d4-49fc-afb7-925552906310\r\nHost: localhost:12047\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 55\r\nCookie: Wl0ksRYl="DWTgfmSZ"\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()

def headWithHeader(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'HEAD /content-types.html HTTP/1.1\r\nContent-Type: text/html\r\nUser-Agent: Client Program\r\nAccept: */*\r\nHost: localhost:12047\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 55\r\nCookie: Wl0ksRYl="DWTgfmSZ"\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()
	
def putWithHeaderAndData(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'PUT /put2.html HTTP/1.1\r\nContent-Type: text/html\r\nUser-Agent: Client Program\r\nAccept: */*\r\nHost: localhost:12047\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 55\r\nCookie: Wl0ksRYl="DWTgfmSZ"\r\n\r\n<html><head></head><body>Put 1</body></html>'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()

def deleteWithHeader(mysock):
	global mutex
	#mutex.acquire()
	cmd = 'DELETE /put1.html HTTP/1.1\r\nContent-Type: text/html\r\nUser-Agent: Client Program\r\nAccept: */*\r\nPostman-Token:\r\na3135fe6-80d4-49fc-afb7-925552906310\r\nHost: localhost:12047\r\nAccept-Encoding: gzip, deflate, br\r\nConnection: keep-alive\r\nContent-Length: 55\r\nCookie: Wl0ksRYl="DWTgfmSZ"\r\n\r\n'.encode()
	mysock.send(cmd)
	data = mysock.recv(1024)
	if len(data) < 1:
		return
	print(data.decode(),end='')
	#mutex.release()



while i < 10:
	#threading.Thread(target = RecvAndSend,args = (connectionSocket,addr)).start()
	mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mysock.connect(('127.0.0.1', 12050))
	#singleGet(mysock)
	t1=threading.Thread(target = singleGet,args = (mysock,)).start()
	t2=threading.Thread(target = singlePost,args = (mysock,)).start()
	t3=threading.Thread(target = getWithHeader,args = (mysock,)).start()
	t4=threading.Thread(target = postWithHeader,args = (mysock,)).start()
	t5=threading.Thread(target = headWithHeader,args = (mysock,)).start()
	t6=threading.Thread(target = putWithHeaderAndData,args = (mysock,)).start()
	t7=threading.Thread(target = deleteWithHeader,args = (mysock,)).start()
	
	i+=1
print("--------------",i)

