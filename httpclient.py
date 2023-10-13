#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")

class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        first_line = data.split("\n", 1)[0]
        code = first_line.split(" ")[1]
        return int(code)        

    def get_headers(self,data):
        return None

    def get_body(self, data):
        lines = data.split("\r\n")
        i = 0
        for line in lines:
            # print(line)
            i+=1
            if line == "":
                break
        body = ''.join(lines[i:])
        return body
    
    def get_host_port_path(self, url):
        temp = url.split('/')
        host_port = temp[2]
        
      
        if ":" in host_port:
            path = ''
            for i in range(3, len(temp)):
                path += "/" + temp[i]
            temp = host_port.split(':')
            host = temp[0]
            port = temp[1]
        else:
            print(host_port)
            path = "/"
            host = host_port
            port = '80'
            
        return host, int(port), path
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        code = 500
        body = ""
        
        # print("------------------------------URL IS: ", url)
        host, port, path = self.get_host_port_path(url)
        print(f"--Host: {host} --Port: {port} --Path: {path}")
        
        # took from lab2 code
        data = f'GET {path} HTTP/1.1\r\nHost: {host}:{port}\r\nConnection: close\r\n\r\n'
        # print(data)
        
        try:
            print("connecting...")
            self.connect(host, port)
            print("connection success!")
        
            print("sending...")
            self.sendall(data)
            print("success")
            
            print("reading...")
            recv_data = self.recvall(self.socket)
            print("finished reading")
            
            # print(recv_data)
            
            code = self.get_code(recv_data)
            body = self.get_body(recv_data)
            # print("code, body:  ")
            # print(code, body)
            
        except:
            code = 404
            print("fail")
        finally:
            print("closing...")
            self.close()
            print("connection closed\n---------------------------------------------\n")
        
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        code = 200
        body = ""
        
        # print("------------------------------URL IS: ", url)
        host, port, path = self.get_host_port_path(url)
        print(f"--Host: {host} --Port: {port} --Path: {path}")
        
        if args == None:
            content_length = 0
            content = ''
        else:
            content_length = len(urllib.parse.urlencode(args))
            content = urllib.parse.urlencode(args)
        
        # took from lab2 code
        data = f'POST {path} HTTP/1.1\r\nHost: {host}:{port}\r\ncontent-type: application/x-www-form-urlencoded\r\nContent-length: {content_length}\r\nConnection: close\r\n\r\n{content}'
        
        try:
            print("connecting...")
            self.connect(host, port)
            print("connection success!")
        
            print("sending...")
            self.sendall(data)
            print("success")
            
            print("reading...")
            recv_data = self.recvall(self.socket)
            print("finished reading")
            
            # print(recv_data)
        
            code = self.get_code(recv_data)
            body = self.get_body(recv_data)
            # print("code, body:  ")
            # print(code, body)
            
        except:
            code = 404
            print("fail")
        finally:
            print("closing...")
            self.close()
            print("connection closed\n---------------------------------------------\n")
        
        return HTTPResponse(code, body)


    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
