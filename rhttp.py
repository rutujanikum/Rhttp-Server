#!/usr/bin/python3
from socket import *
import sys
from datetime import datetime, timedelta
from time import strftime,gmtime
from pymemcache.client import base
import os.path, time
import os
from os import path
import threading
import random
import string
import re

clients = 0
key=""
cookie_val=""
cookieExp=""
sentence = ""
cookie_expiry=""

#GENERATE RANDOM STRING FOR COOKIES
def get_random_alphanumeric_string():
	length = random.randint(6,9)
	letters_and_digits = string.ascii_letters + string.digits
	result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
	return result_str
   
#------------------------------FUCTIONS FOR REQUEST METHOD IMPLEMENTATION------------------------------

def getMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr):
	global key
	global cookie_val
	global cookieExp
	global cookie_expiry
	global sentence
	text=""
	filename=location[1:]
	string = "HTTP/1.1 200 OK\r\n"
	accessLogdata += " 200 "
	string += "Date: "+dt_string+"\r\n"
	string += "Server: localhost/127.0.0.1 (Ubuntu)\r\n"
	location = DocumentRoot+location
	if(path.exists(str(location)) and ext != "ico"):
		if(os.access(location, os.R_OK)):
			#print("YOu can read file")
			f = open(location,'rb')
			text = f.read()
			f.close()
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			#csv,pdf,zip, if modified since				
			if(ext == "html"):
				string += "Content-Type: text/html; charset=iso-8859-1\r\n"
			elif(ext == "txt"):
				string += "Content-Type: text/plain; charset=iso-8859-1\r\n"
			elif(ext == "csv"):
				string += "Content-Type: text/csv; charset=iso-8859-1\r\n"
			elif(ext == "pdf"):
				string += "Content-Type: application/pdf; charset=iso-8859-1\r\n"
			elif(ext == "zip"):
				string += "Content-Type: application/zip; charset=iso-8859-1\r\n"
			elif(ext == "png" or ext == "jpeg" or ext == "jpg"):
				string += "Content-Type: image/jpg; charset=iso-8859-1\r\n"
			elif(ext == "movie" or ext == "mp4" or ext == "avi"):
				string += "Content-Type: video/mp4; charset=utf-8\r\n"
			elif(ext == "ogg" or ext == "mp3"):
				string += "Content-Type: audio/ogg; charset=utf-8\r\n"
			elif(ext == "xml"):
				string += "Content-Type: text/xml; charset=iso-8859-1\r\n"
			else:
				string += "Content-Type: text/html; charset=utf-8\r\n"
			if(cookieExp == 1):
				string += "Set-Cookie: "+key+"=\""+cookie_val+"\"; Expires=\""+cookie_expiry+"\"\r\n" 
			string += "Last-Modified: "+str(time.ctime(os.path.getmtime(location)))+"\r\n"
		else:
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " (13)Permission denied: [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH00132: file permissions deny server access:/ "+filename+"\n"
			f = open("rhttp/error/403.html",'rb')
			text = f.read()
			f.close();
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			string += "Content-Type: text/html; charset=iso-8859-1\r\n" 		
	elif(ext != "ico"):
		errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
		errorLogdata += " [core:info]"
		errorLogdata += " [pid "+str(os.getpid())
		errorLogdata += ":tid "+str(threading.get_ident())+"]"
		errorLogdata += " [client "+str(addr[0])+": "+str(addr[1])+"]"
		errorLogdata += " AH00128: File does not exist:/ "+filename+"\n"
		f = open("rhttp/error/404.html",'rb')
		text = f.read()
		f.close();
		string += "Content-Length: "+str(len(text))+"\r\n"
		accessLogdata += str(len(text)).rstrip()
		string += "Content-Type: text/html; charset=iso-8859-1\r\n"
			
	string += "Connection: close\r\n"			
	string += "\r\n"
	output = string.encode() + text
	return output, accessLogdata, errorLogdata
	
def postMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr):
	global key
	global cookie_val
	global cookieExp
	global cookie_expiry
	global sentence
	text=""
	filename=location[1:]
	body = sentence.split("\r\n\r\n")
	body = body[1]
	string = "HTTP/1.1 200 OK\r\n"
	accessLogdata += " 200 "
	string += "Date: "+dt_string+"\r\n"
	string += "Server: localhost/127.0.0.1 (Ubuntu)\r\n"
	location = DocumentRoot+location
	if(path.exists(str(location)) and ext != "ico"):
		if(os.access(location, os.R_OK)):
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " mod_authz_core.c(817): [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH01626: authorization result of Require all granted: granted\n"
			f = open(location,'rb')
			text = f.read()
			f.close()
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()				
			if(ext == "html"):
				string += "Content-Type: text/html; charset=iso-8859-1\r\n"
			elif(ext == "txt"):
				string += "Content-Type: text/plain; charset=iso-8859-1\r\n"
			elif(ext == "csv"):
				string += "Content-Type: text/csv; charset=iso-8859-1\r\n"
			elif(ext == "pdf"):
				string += "Content-Type: application/pdf; charset=iso-8859-1\r\n"
			elif(ext == "zip"):
				string += "Content-Type: application/zip; charset=iso-8859-1\r\n"
			elif(ext == "png" or ext == "jpeg" or ext == "jpg"):
				string += "Content-Type: image/jpg; charset=iso-8859-1\r\n"
			elif(ext == "movie" or ext == "mp4" or ext == "avi"):
				string += "Content-Type: video/mp4; charset=utf-8\r\n"
			elif(ext == "ogg" or ext == "mp3"):
				string += "Content-Type: audio/ogg; charset=utf-8\r\n"
			elif(ext == "xml"):
				string += "Content-Type: text/html; charset=iso-8859-1\r\n"
			string += "Last-Modified: "+str(time.ctime(os.path.getmtime(location)))+"\r\n" 	
		else:
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " (13)Permission denied: [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH00132: file permissions deny server access:/ "+filename+"\n"
			text = f.read()
			f.close();
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			string += "Content-Type: text/html; charset=iso-8859-1\r\n" 		
	else:
		errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
		errorLogdata += " [core:info]"
		errorLogdata += " [pid "+str(os.getpid())
		errorLogdata += ":tid "+str(threading.get_ident())+"]"
		errorLogdata += " [client "+str(addr[0])+": "+str(addr[1])+"]"
		errorLogdata += " AH00128: File does not exist:/ "+filename+"\n"
		f = open("rhttp/error/404.html",'rb')
		text = f.read()
		f.close();
		string += "Content-Length: "+str(len(text))+"\r\n"
		accessLogdata += str(len(text)).rstrip()
		string += "Content-Type: text/html; charset=iso-8859-1\r\n"

	string += "Connection: close\r\n"			
	string += "\r\n"
	output = string.encode() + text
	return output, accessLogdata, errorLogdata
	
	
def putMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr):
	global key
	global cookie_val
	global cookieExp
	global cookie_expiry
	global sentence
	filename=location[1:]	
	text=""
	body = sentence.split("\r\n\r\n")
	body = body[1]
	if(location != "/"):
		path_w = DocumentRoot+location
		if(path.exists(str(path_w))):
			#FILE MODIFIED NOT CREATED
			string = "HTTP/1.1 204 NO CONTENT\r\n"
			accessLogdata += " 204 "
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " mod_authz_core.c(817): [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH01626: authorization result of Require all granted: granted\n"
		else:
			string = "HTTP/1.1 201 CREATED\r\n"
			accessLogdata += " 201 "
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " mod_authz_core.c(817): [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH01626: authorization result of Require all granted: granted\n"
		string += "Content-Location: /"+path_w+"\r\n"
		if(ext != "ico"):
			f1 = open(path_w,'w')
			f1.write(body)
		accessLogdata += str(len(body)).rstrip()
			
		#NO CONTENT-LENGHT AND CONTENT-TYPE FOR PUT RESPONSE				

		string += "Connection: close\r\n"			
		string += "\r\n"
		
		print(string)
		try:
			output = string.encode()
			connectionSocket.sendall(output)
		except Exception as exc :
			print("Error:");
			print(exc)
		#connectionSocket.send(text)
	else:
		errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
		errorLogdata += " [core:error]"
		errorLogdata += " [pid "+str(os.getpid())
		errorLogdata += ":tid "+str(threading.get_ident())+"]"
		errorLogdata += " [client "+str(addr[0])+": "+str(addr[1])+"]"
		errorLogdata += " AH00147: Empty File Path:\n"
		string = "HTTP/1.1 400 BAD REQUEST\r\n"
		accessLogdata += " 400 "
		string += "Date: "+dt_string+"\r\n"
		string += "Server: localhost/127.0.0.1 (Ubuntu)\r\n"
		if(ext != "ico"):
			f = open("rhttp/error/400.html",'rb')
			text = f.read()
			f.close()
		string += "Connection: close\r\n"			
		string += "\r\n"
	
	output = string.encode() + text
	return output, accessLogdata, errorLogdata
	

def headMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr):
	global key
	global cookie_val
	global cookieExp
	global cookie_expiry
	global sentence
	text=""
	filename=location[1:]	
	string=""
	text=""
	string = "HTTP/1.1 200 OK\r\n"
	accessLogdata += " 200 "
	string += "Date: "+dt_string+"\r\n"
	string += "Server: localhost/127.0.0.1 (Ubuntu)\r\n"
	location = DocumentRoot+location
	if(path.exists(str(location)) and ext != "ico"):
		if(os.access(location, os.R_OK)):
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " mod_authz_core.c(817): [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH01626: authorization result of Require all granted: granted\n"
			f = open(location,'rb')
			text = f.read()
			f.close();
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			#csv,pdf,zip, if modified since				
			if(ext == "html"):
				string += "Content-Type: text/html; charset=iso-8859-1\r\n"
			elif(ext == "txt"):
				string += "Content-Type: text/plain; charset=iso-8859-1\r\n"
			elif(ext == "csv"):
				string += "Content-Type: text/csv; charset=iso-8859-1\r\n"
			elif(ext == "pdf"):
				string += "Content-Type: application/pdf; charset=iso-8859-1\r\n"
			elif(ext == "zip"):
				string += "Content-Type: application/zip; charset=iso-8859-1\r\n"
			elif(ext == "png" or ext == "jpeg" or ext == "jpg"):
				string += "Content-Type: image/jpg; charset=utf-8\r\n"
			elif(ext == "movie" or ext == "mp4" or ext == "avi"):
				string += "Content-Type: video/mp4; charset=utf-8\r\n"
			elif(ext == "ogg" or ext == "mp3"):
				string += "Content-Type: audio/ogg; charset=utf-8\r\n"
			elif(ext == "xml"):
				string += "Content-Type: text/html; charset=utf-8\r\n"
			else:
				string += "Content-Type: text/html; charset=utf-8\r\n"
			if(cookieExp == 1):
				string += "Set-Cookie: "+key+"=\""+cookie_val+"\"; Expires=\""+cookie_expiry+"\"\r\n" 
			string += "Last-Modified: "+str(time.ctime(os.path.getmtime(location)))+"\r\n" 
		else:
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " (13)Permission denied: [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH00132: file permissions deny server access:/ "+filename+"\n"
			f = open("rhttp/error/403.html",'rb')
			text = f.read()
			f.close();
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			string += "Content-Type: text/html; charset=iso-8859-1\r\n" 	

	else:
		errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
		errorLogdata += " [core:info]"
		errorLogdata += " [pid "+str(os.getpid())
		errorLogdata += ":tid "+str(threading.get_ident())+"]"
		errorLogdata += " [client "+str(addr[0])+": "+str(addr[1])+"]"
		errorLogdata += " AH00128: File does not exist:/ "+filename+"\n"
		f = open("rhttp/error/404.html",'rb')
		text = f.read()
		f.close();
		string += "Content-Length: "+str(len(text))+"\r\n"
		accessLogdata += str(len(text)).rstrip()
		string += "Content-Type: text/html; charset=iso-8859-1\r\n"
	
	string += "Connection: close\r\n"			
	string += "\r\n"
	
	connectionSocket.sendall(string.encode())
	#connectionSocket.send(text)
	
	return string, accessLogdata, errorLogdata


def deleteMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr):
	global key
	global cookie_val
	global cookieExp
	global cookie_expiry
	global sentence
	text=""
	string=""
	filename=location[1:]	
	if(location != "/"):
		string = "HTTP/1.1 200 OK\r\n"
		accessLogdata += " 200 "
		string += "Date: "+dt_string+"\r\n"
		string += "Server: localhost/127.0.0.1 (Ubuntu)\r\n"
		location = DocumentRoot+location
		if(path.exists(str(location))):
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:error]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " mod_authz_core.c(817): [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH01626: authorization result of Require all granted: granted\n"
			if(ext != "ico"):
				f = open(location,'rb')
				text = f.read()
				f.close();
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			if(ext == "html"):
				string += "Content-Type: text/html; charset=iso-8859-1\r\n"
			elif(ext == "txt"):
				string += "Content-Type: text/plain; charset=iso-8859-1\r\n"
			elif(ext == "csv"):
				string += "Content-Type: text/csv; charset=iso-8859-1\r\n"
			elif(ext == "pdf"):
				string += "Content-Type: application/pdf; charset=iso-8859-1\r\n"
			elif(ext == "zip"):
				string += "Content-Type: application/zip; charset=iso-8859-1\r\n"
			elif(ext == "png" or ext == "jpeg" or ext == "jpg"):
				string += "Content-Type: image/jpg; charset=utf-8\r\n"
			elif(ext == "movie" or ext == "mp4" or ext == "avi"):
				string += "Content-Type: video/mp4; charset=utf-8\r\n"
			elif(ext == "ogg" or ext == "mp3"):
				string += "Content-Type: audio/ogg; charset=utf-8\r\n"
			elif(ext == "xml"):
				string += "Content-Type: text/html; charset=utf-8\r\n"
			if(cookieExp == 1):
					string += "Set-Cookie: "+key+"=\""+cookie_val+"\"; Expires=\""+cookie_expiry+"\"\r\n" 
			string += "Last-Modified: "+str(time.ctime(os.path.getmtime(location)))+"\r\n" 	
			try:
				os.remove(location)
			except:
				errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
				errorLogdata += " [core:error]"
				errorLogdata += " [pid "+str(os.getpid())
				errorLogdata += ":tid "+str(threading.get_ident())+"]"
				errorLogdata += " (13)Permission denied: [client "+str(addr[0])+": "+str(addr[1])+"]"
				errorLogdata += " AH00132: file permissions deny server access:/ "+filename+"\n"
				f = open("rhttp/error/403.html",'rb')
				text = f.read()
				f.close();
				string += "Content-Length: "+str(len(text))+"\r\n"
				accessLogdata += str(len(text)).rstrip()
				string += "Content-Type: text/html; charset=iso-8859-1\r\n" 
		else:
			errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			errorLogdata += " [core:info]"
			errorLogdata += " [pid "+str(os.getpid())
			errorLogdata += ":tid "+str(threading.get_ident())+"]"
			errorLogdata += " [client "+str(addr[0])+": "+str(addr[1])+"]"
			errorLogdata += " AH00128: File does not exist:/ "+filename+"\n"
			f = open("rhttp/error/404.html",'rb')
			text = f.read()
			f.close();
			string += "Content-Length: "+str(len(text))+"\r\n"
			accessLogdata += str(len(text)).rstrip()
			string += "Content-Type: text/html; charset=utf-8\r\n"
		string += "Connection: close\r\n"			
		string += "\r\n"
	else:
		errorLogdata = "["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
		errorLogdata += " [core:error]"
		errorLogdata += " [pid "+str(os.getpid())
		errorLogdata += ":tid "+str(threading.get_ident())+"]"
		errorLogdata += " [client "+str(addr[0])+": "+str(addr[1])+"]"
		errorLogdata += " AH00147: Empty File Path:\n"
		string = "HTTP/1.1 400 BAD REQUEST\r\n"
		accessLogdata += " 400 "
		string += "Date: "+dt_string+"\r\n"
		string += "Server: localhost/127.0.0.1 (Ubuntu)\r\n"
		if(ext != "ico"):
			f = open("rhttp/error/400.html",'rb')
			text = f.read()
			f.close()
		string += "Connection: close\r\n"			
		string += "\r\n"
	output = string.encode() + text
	return output, accessLogdata, errorLogdata


#------------------------------------------------------------------------------------------------------


#--------------SERVER CODE START---------------------#
def acceptReq(serverSocket):
	global clients
	while True:
		connectionSocket, addr = serverSocket.accept()
		print("new request received from"); print(addr);
		print("connectionSocket is"); print(connectionSocket); 
		clients += 1
		print("Number of clients=================>",clients)
		threading.Thread(target = RecvAndSend,args = (connectionSocket,addr)).start()

def RecvAndSend(connectionSocket,addr):
	global DocumentRoot
	global errorlog
	global accesslog
	global maxreq
	global key
	global cookie_val
	global cookieExp
	global sentence
	while True:
		try:
			sentence = connectionSocket.recv(1024).decode()
			words = sentence.split("\n")
			header_len = len(words)
			client = base.Client(('localhost',11211))
			referer = ""
			cookie_val = ""
			key = ""
			key_temp=""
			user_agent=""
			text=""
			cookieExp=1
			ext=""
			host=""
			accessLogdata=""
			errorLogdata=""
			filename=""
			if ( len(words) > 1 ) :
				print("----REQUEST----") 
				i = 0
				while(i < len(words)):		
					print(words[i])
					if(words[i][:8] == "Referer:"):
						referer = " \""+words[i][9:].rstrip()+"\""
					if(words[i][:5] == "Host:"):
						host = words[i][6:].rstrip()
					if(words[i][:11] == "User-Agent:"):
						user_agent=words[i][11:].rstrip()
					if(words[i][:7] == "Cookie:"):
						key_temp=re.split("=| ",words[i])
						key = key_temp[1].split("= ")
						j = 1
						# CHECK FOR ALL COOKIES IN REQUEST
						while(j < len(key_temp)):
							key = key_temp[j].strip()
							j += 2
							res1 = client.get(key)
							if res1 is None:
								#Cookie not present
								cookieExp=1
							else:
								#Cookie present
								cookieExp=0	
								break						
					i += 1
			
			#GET LOCATION AND EXTENSION OF REQUESTED FILE
			try:
				temp = words[0].split(" ")
				location = temp[1]
				if(location == "/"):
					location = "/index.html"
				else:
					#location = location[1:]
					ext = location.split(".")
					if(len(ext)>1):
						ext = ext[1]
					else:
						ext=""
				filename = location[1:]
			except Exception as exc :
				pass
				
			#---------------------------------------------
			
			
			#GET DATETIME FOR ACCESS LOG AND COOKIE
			now = datetime.now()
			expires = datetime.now() + timedelta(7)
			dt_string = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
			cookie_expiry = expires.strftime("%a, %d %b %Y %H:%M:%S GMT")
			#HANDLE FILES WITHOUT EXTENSION(REAMINING)
			accessLogdata = host.rstrip()
			accessLogdata += " -"
			accessLogdata += " -"
			accessLogdata += " ["+now.strftime("%d/%b/%Y:%H:%M:%S ")+strftime("%z", gmtime())+"]"
			accessLogdata += " \""+words[0].rstrip()+"\""
			accessLogdata += referer			
			
			#------------------------------------------
			
			
			#----CHACHE-------
			if(cookieExp == 1):
				key=get_random_alphanumeric_string()
				cookie_val = get_random_alphanumeric_string()
				client.set(key,cookie_val)
			#-----------------


			if(temp[0] == "GET"):
				try:
					output, accessLogdata, errorLogdata = getMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr)
					connectionSocket.sendall(output)
				except Exception as exc :
					print("Error:");
					print(exc)

			elif(temp[0] == "PUT"):
					
				try:
					output, accessLogdata, errorLogdata = putMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr)
					connectionSocket.sendall(output)
				except Exception as exc :
					print("Error:");
					print(exc)
				

			elif(temp[0] == "POST"):
				try:
					output, accessLogdata, errorLogdata = postMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr)
					connectionSocket.sendall(output)
				except Exception as exc :
					print("Error:");
					print(exc)
				

			elif(temp[0] == "HEAD"):
				try:
					output, accessLogdata, errorLogdata = headMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr)
					#connectionSocket.sendall(output.encode())
				except Exception as exc :
					print("Error:");
					print(exc)

			elif(temp[0] == "DELETE"):
				try:
					output, accessLogdata, errorLogdata = deleteMethod(accessLogdata, errorLogdata, dt_string, location, DocumentRoot, ext, connectionSocket, now, addr)
					connectionSocket.sendall(output)
				except Exception as exc :
					print("delete Error:");
					print(exc)
			

				
#------------------------------WRITING LOG FILES------------------------------------
				
			accessLogdata += " \""+user_agent.rstrip()+"\""+"\n"
			if(len(words) > 1):
				if(path.exists(str(accesslog))):
					access_log = open(accesslog,'a')
					access_log.write(accessLogdata)
					access_log.close()
				else:
					access_log = open(accesslog,'wb')
					access_log.write(accessLogdata)
					access_log.close()
				
				if(path.exists(str(errorlog))):
					access_log = open(errorlog,'a')
					access_log.write(errorLogdata)
					access_log.close()
				else:
					access_log = open(errorlog,'wb')
					access_log.write(errorLogdata)
					access_log.close()
					
#------------------------------------LOG END---------------------------------------------
			
		except Exception as exc :
			print("Error:\n");
			print(exc)
			connectionSocket.close()
			return False
#--------------SERVER CODE END---------------------#


#READ CONFIGURATIONS FROM RHTTP.CONF FILE

DocumentRoot = ""
port = ""
errorlog = ""
accesslog = ""
maxreq = ""
f = open("rhttp.conf",'r')
text = f.read()
f.close();
text = text.split("\n")
i = 0
while(i < len(text)):
	if(text[i][:12] == "DocumentRoot"):
		DocumentRoot = text[i][13:]
	elif(text[i][:6] == "LISTEN"):
		port = int(text[i][7:])
	elif(text[i][:8] == "ErrorLog"):
		errorlog = text[i][9:]
	elif(text[i][:9] == "AccessLog"):
		accesslog = text[i][10:]
	elif(text[i][:23] == "MaxSimultaneousRequests"):
		maxreq = text[i][24:]
	i+=1
serverSocket = socket(AF_INET, SOCK_STREAM)
#the server opens a socket but must bind it to the port
try:
	serverPort = int(port)
	serverSocket.bind(('',serverPort))
	#after that server listens waits for someone to send a connection request.
	serverSocket.listen(1)
	print("The server is ready to receive on PORT ["+str(serverPort)+"]") 
	acceptReq(serverSocket)
		
except KeyboardInterrupt :
	print("\nShutting down...\n");
except Exception as exc :
	print("Error:\n");
	print(exc)

serverSocket.close();
#connectionSocket.close()
