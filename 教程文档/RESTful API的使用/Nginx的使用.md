# Nginx 的使用
## 1、Nginx 是什么？
Nginx 是一个高性能的 HTTP 和反向代理服务器，它也可以用作 IMAP/POP3 代理服务器。  
Nginx 以其高性能、稳定性和丰富的功能而闻名，特别适合处理高并发请求。它被广泛用于以下场景：
* Web 服务器：提供静态和动态内容的托管和分发。
* 反向代理：将请求转发给后端的 Web 应用服务器（如 Flask、Django 等）。
* 负载均衡：将流量分发到多个后端服务器，以实现高可用性和性能。
* CDN：作为内容分发网络的一部分，缓存和分发静态内容。

## 2、Nginx 的使用步骤，只针对 Linux 系统
### 2.1、Linux 上安装，Ubuntu/Debian
```bash
sudo apt update
sudo apt install nginx
```
### 2.2、启动和停止 Nginx
```bash
sudo service nginx start # 启动
sudo service nginx stop # 停止
sudo service nginx restart # 重启
```
### 2.3、配置 Nginx  
配置文件通常位于 /etc/nginx/nginx.conf  
编辑配置文件以设置 Nginx 的行为。以下是一个基本的Web服务器配置示例：  
```nginx
server {
    listen 80;
    server_name localhost;

    # 静态文件目录
    location / {
        root /var/www/html;
        index index.html index.htm;
    }

    # 转发请求到后端服务器
    location /api {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 错误页面
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /var/www/html;
    }
}
```

```bash
sudo nginx -t # 保存配置文件后，测试配置是否正确
sudo systemctl reload nginx # 如果配置正确，重新加载Nginx以应用更改
```
### 2.4、使用 Nginx 作为反向代理
1、配置反向代理  
编辑配置文件以设置反向代理。例如，将请求转发给 Flask 应用：  
```nginx
server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
2、保存并重新加载 Nginx  
保存配置文件后，重新加载 Nginx 以应用更改：  
```bash
sudo systemctl reload nginx
```
### 2.5、设置负载均衡
1、配置负载均衡：  
编辑配置文件以设置负载均衡。例如，将流量分发到多个后端服务器：
```nginx
upstream backend {
    server 192.168.1.1:8000;
    server 192.168.1.2:8000;
    server 192.168.1.3:8000;
}

server {
    listen 80;
    server_name localhost;

    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
2、保存并重新加载 Nginx：  
保存配置文件后，重新加载 Nginx 以应用更改：  
```bash
sudo systemctl reload nginx
```