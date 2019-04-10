import socket
import threading
import Tools
bind_ip = "192.168.2.210"  #监听所有可用的接口
bind_port = 9999   #非特权端口号都可以使用

#AF_INET：使用标准的IPv4地址或主机名，SOCK_STREAM：说明这是一个TCP服务器
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#服务器监听的ip和端口号
server.bind((bind_ip,bind_port))
server.listen(5000)
print("[*] Listening on %s:%d" % (bind_ip,bind_port))

data_tools = Tools.DataTools()
print('Runing wait to end')
data_tools.Run()
print('Runing end')

len1 = data_tools.one_gram_counts
dic1 = data_tools.get_one_dic()

len2 = data_tools.two_gram_counts
dic2 = data_tools.get_2_dic()

len3 = data_tools.three_gram_counts
dic3 = data_tools.get_3_dic()


def handle_client(client_socket):
    try:
        while True:
            resp=""
            request = client_socket.recv(1024)
            print("[*] Received: %s" % request.decode('utf-8'))        #向客户端返回数据
            msg = request.decode('utf-8').strip()
            if msg == 'EXIT':
                client_socket.close()
                break
            elif msg == '1_LEN':
                resp = len1
            elif msg == '2_LEN':
                resp = len2
            elif msg == '3_LEN':
                resp = len3
            else:
                ngram,word = msg.split('_')
                try :
                    if ngram == "1":
                        if word in dic1:
                            resp = dic1[word]
                        else:
                            resp = "None"
                    elif ngram == "2":
                        if word in dic2:
                            resp = dic2[word]
                        else:
                            resp = "None"
                    elif ngram == "3":
                        if word in dic3:
                            resp = dic3[word]
                        else:
                            resp = "None"
                except Exception as e:
                    resp="Error"
                    print(str(e))
            client_socket.send(resp.encode('utf-8'))
    except Exception as e:
                print(str(e))

try:
    while True:
        try:
            #等待客户连接，连接成功后，将socket对象保存到client，将细节数据等保存到addr
            client,addr = server.accept()
            print("[*] Acception connection from %s:%d" % (addr[0],addr[1]))
            client_handler = threading.Thread(target=handle_client,args=(client,))
            client_handler.start()
        except Exception as e:
            print(str(e))
except Exception as e:
    print(e)
    server.close()
