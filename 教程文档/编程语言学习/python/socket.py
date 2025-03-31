import socket

socket_server = socket.socket() # 创建一个socket对象
socket_server.bind(("localhost", 9999)) # 绑定IP和端口
socket_server.listen(5) # 监听端口，最大连接数为5
print("Server is listening on port 9999") 
client, addr = socket_server.accept() # 接受客户端的连接
print("Got connection from", addr)

while True: 
    data = client.recv(1024).decode("utf-8") # 接收客户端的消息
    print("Client's message is:", data) 
    msg = input("Enter your message:").encode("utf-8") # 输入消息
    if msg == "exit": # 如果输入 exit，则退出
        break
    client.send(msg) # 发送消息给客户端
client.close() # 关闭客户端连接
socket_server.close() # 关闭服务器连接
