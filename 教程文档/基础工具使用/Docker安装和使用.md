# Docker 的安装和使用
## （1）**Docker 简介**
Docker 是一种开源的容器化技术，它允许开发者将应用及其依赖打包到一个轻量级、可移植的容器中，然后可以在任何支持 Docker 的机器上运行这个容器。Docker 容器可以在虚拟机、物理机、云平台等多种环境中运行，极大地提高了软件部署的灵活性和效率。

1. Docker 的核心概念  
* **镜像（Image）**：Docker 镜像是构建 Docker 容器的模板，它是一个只读的文件系统，包含了运行容器所需的程序、库、资源、配置等文件。镜像可以通过 Dockerfile 来定义，并且支持层级结构，这意味着可以使用已有的镜像作为基础，再添加新的层来定制自己需要的环境。

* **容器（Container）**：容器是镜像的运行实例。它与直接在宿主机上运行的进程不同，容器进程运行在独立的命名空间中，拥有自己的文件系统、网络配置、进程空间等。容器可以被创建、启动、停止、删除、暂停等，是应用运行的动态实体。

* **仓库（Repository）**：Docker 仓库用于集中存放镜像文件，类似于代码仓库。它可以是公开的也可以是私有的，支持镜像的上传和下载。Docker Hub 是最常用的公开 Docker 仓库，提供了大量的官方和社区镜像。

2. Docker 和虚拟机的区别
* Docker 容器与传统的虚拟机相比，具有资源占用少、启动快速、高效率等优点。容器直接运行在宿主机的内核上，不需要额外的操作系统支持，因此启动速度快，资源开销小。而虚拟机则需要完整的操作系统支持，资源开销较大。

3. Docker 的优势
* **模块化**：Docker 支持微服务架构，可以单独更新或修复应用的某一部分，而不需要停止整个应用。

* **层和镜像版本控制**：Docker 镜像由多个层组成，每个层都可以重用，加快了构建过程。镜像的每一次更改都会创建一个新层，提供了内置的版本控制功能。

* **快速部署**：Docker 容器可以在几秒钟内启动，大大缩短了应用的部署时间。

## （2）**Windows11 安装 Docker**
### （2.1）**Windows 子系统中安装 ubuntu 20.4**
由于 Docker 运行时需要 Linux 的内核，所以需要先在 Windows11 安装 Linux ，这里是在Windows 的子系统下安装 Linux ，不用虚拟机，也不用双系统。  
主要是借助 WSL(windows subsystem for linux)，即 windows 的一个子系统，其作用是在windows 下运行 linux 操作系统。

1. 检查电脑是否支持安装。  
windows 机器需要支持虚拟化，并且需要在 BIOS 中开启虚拟化技术，因为 WSL2 基于 hyper-V。  
要查看是否开启虚拟化，需要 Windows+R 输入 cmd 打开命令行，输入 `systeminfo`  
如果看到如下字样，代表电脑已经支持虚拟化，可继续安装。
```
Hyper-V 要求:     虚拟机监视器模式扩展: 是
                  固件中已启用虚拟化: 是
                  二级地址转换: 是
                  数据执行保护可用: 是
```

2. 打开 "开发人员模式" 和 "适用于 Linux 的 Windows 子系统"
* 在设置中搜索 "开发者" ，找到 "开发人员模式" ，将其打开。安装完后再关闭。

* 找到 `控制面板-程序和功能-启用或关闭 Windows 功能` ，选中 "适用于 Linux 的 Windows 子系统"，然后点击确定。会提示重启电脑，进行重启。

3. 安装 Linux 分发版并升级 WSL 内核
* 以管理员身份运行 PowerShell 或 Windows 命令提示符，输入 `wsl --install` 命令，然后**重启计算机**。  

* **升级 WSL 内核**。适用于 x64 计算机的 WSL2 Linux 内核更新包下载地址：https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi ，下载后双击，依次点击安装即可。

4. 启用虚拟机功能，设置 WSL2 为默认版本
* **启用虚拟机功能**。安装 WSL2 之前，必须启用 "虚拟机平台" 可选功能。 计算机需要虚拟化功能才能使用此功能。以管理员身份打开 PowerShell 并运行下面代码：
```
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```
运行代码之后需要重启，重启即可。

* **设置 WSL2 为默认版本**。打开 powershell ，执行下面的代码将 WSL2 设置为默认版本
```
wsl --set-default-version 2
```

5. 安装 ubuntu 20.4 。
* 打开微软商店（Microsoft store），搜索 ubuntu ，选择 ubuntu 20.4 安装即可。  
完成后可在 `开始` 菜单看到 ubuntu 20.4 的图标，第一次打开需要设置账户名和密码，设置完成后即可进入 ubuntu 。  
至此，ubuntu 20.4 已安装在 Windows11 ，可在 `此电脑` 中看到 Linux 。如果觉得有必要还可以进一步安装桌面环境。

### （2.2）**Windows11 安装 Docker**
* [docker 官网](https://www.docker.com/) 下载对应的 Windows 版本，即 `Windows AMD 64` 版本，下载完成后双击安装即可。  
默认安装路径是 `C:\Program Files\Docker\Docker` ，安装完成即可使用 Docker 。  
如果没有科学上网，下载国外仓库的镜像可能会非常缓慢，甚至无法访问，感觉有必要可以切换镜像源为国内的一些仓库，如阿里云。  
而且有很多仓库都可能失效，搜索还在维护且可使用的进行切换。

## （3）**Docker 的使用**
### （3.1）**Docker 常用命令**
docker 官方帮助文档的地址：<https://docs.docker.com/reference/cli/docker/>

**基础命令**：
```
docker version      # 显示 docker 的版本信息
docker info         # 显示 docker 的系统信息，包括镜像和容器的数量。
docker 命令 --help   # 显示命令的帮助信息，很有用。
```

**镜像命令：**
```
docker images    # 显示当前主机本地的所有镜像
    可选项：    -a 或 --all       # 显示所有信息
               -f 或 --filter    # 过滤
               -q 或 --quiet    # 只显示镜像的 id

docker search 镜像名    # 从 dockerHub 官网搜索镜像
docker pull 镜像名      # 从远程仓库拉取镜像，默认从官方仓库，配置了国内源则使用国内源，更快，
    默认 pull 的是最新版，也可以指定 tag 下载对应的版本，比如 docker pull mysql:5.7 ， 
    下载时是分层下载，分层可以节省空间，许多镜像的一些层都可以共用，所以不用重复下载。
docker rmi -f 镜像名或id  # rmi 即 remove images ， f 即 force 。
    比如： docker rmi -f $(docker images -aq) ， 即查到所有镜像的 id ，然后强制删除。
```

**容器命令**
```
# 首先下载一个镜像
docker pull centos

# 运行镜像之后产生容器
docker run 可选参数 镜像名或id
    可选参数：
        --name="name"   # 指定容器名字
        -d 或 --detach  # 后台运行
        -it             # interactive(交互式运行)，进入容器查看内容
            比如： docker run -it centos /bin/bash 打开并进入容器 centos ，执行 exit 退出容器。
        -p              # 小写 p ，指定容器的端口
            -p 常用方式为： -p 主机端口：容器端口
        -P              # 大写 P ，随机指定端口

docker ps       # 列出所有正在运行的容器
docker ps -a    # 列出所有运行过的容器

# 退出容器
exit            # 直接停止容器并退出
Ctrl + p + q    # 退出但不停止容器

# 删除容器，和删除镜像类似
docker rm 容器名或id            # 删除指定容器，不能删除正在运行的容器
docker rm -f 容器名或id         # 强制删除指定容器
docker rm -f $(docker ps -aq)  # 强制删除所有容器

# 启动、重启容器
docker start 容器名或id    # 启动容器
docker restart 容器名或id  # 重启容器
docker stop 容器名或id     # 停止正在运行的容器
docker kill 容器名或id     # 强制停止运行的容器
```

**常用其它命令**
```
docker run -d 镜像名或id    # 后台运行镜像，但前提是还有前台进程，不然后台的会被关闭。

# 查看日志
docker logs -tf --tail 10 容器名或id            # 日志可能为空，就没有内容来显示

# 重新关闭容器再运行以下
docker run -d centos /bin/sh -c "echo dsc;"    # 后台运行 centos 并使用 shell 输入内容 "echo dsc;"，作用是打印出 dsc 。
docker logs -tf --tail 10 容器名或id            # 再次执行就会输出日志内容 dsc 

# 查看镜像元数据
docker inspect 容器名或id

# 进入当前正在运行的容器，修改某些配置
# 方法 1 ，进入容器后开启一个新的终端，可以在里面操作，较常用。
docker exec -it 容器名或id bash或shell    # exec 即 execute
    比如: docker exec -it 容器名或id /bin/bash

# 方法 2 ，进入容器正在执行的终端，不会启动新的进程。
docker attach 容器名或id 

# 将容器内的文件复制到主机内，注意此命令在主机内运行，容器内可能不支持。
docker cp 容器名或id:容器内的路径 主机的路径
    比如： docker cp 2374b602f474:/home/name.txt /home/dsc/dockerFile  
```

**镜像修改和上传到远程仓库**
```
# 有些镜像修改之后需要另存，使用 docker commit 命令
# 注意镜像只能运行为容器之后才能重新保存。
docker commit -a="dsc" -m="the first commit" 要上传的容器名或id 上传后的镜像名:版本号
    比如： docker commit -a="dsc" -m="the first commit" hello-world hello-world02:v2.0
            就是将修改后的 hello-world 容器上传到本地并重命名为 hello-world02 镜像，版本号为 v2.0
            -a 是上传者， -m 是备注

# 可以将镜像重新命名进行复制保存
docker tag 原来的镜像名或id:版本号 重命名后的镜像名或id:版本号
    比如： docker tag centos01:V1.0 centos02:V2.0    就会生成新的镜像 centos02 ，版本号为 V2.0

# 上传镜像到阿里云镜像仓库
# 首先需要注册阿里云，然后搜索容器镜像服务，新建命名空间和仓库，仓库中会有如何上传的教程。

# 1、登录账号 ，需要输入密码
docker login --username=DSC小南 crpi-287rcr0qlapyqwl1.cn-chengdu.personal.cr.aliyuncs.com
# 2、打标签
docker tag 输入镜像id crpi-287rcr0qlapyqwl1.cn-chengdu.personal.cr.aliyuncs.com/docker-dsc/test:输入镜像版本号
# 3、推送到阿里云仓库
docker push crpi-287rcr0qlapyqwl1.cn-chengdu.personal.cr.aliyuncs.com/docker-dsc/test:输入镜像版本号
```

### （3.2）**Docker 容器数据卷**
容器之间可以数据共享，容器中产生的数据，可以同步到本地。  
简单说就是目录的挂载，将容器内的目录挂载到其它容器或宿主机 Linux 中  
好处是若要修改容器内的内容，只需要在本地修改，容器内就会同步数据，只要容器没有被删除。  
而且删除容器之后，本地的数据也不会丢失。

**指定路径挂载、具名挂载和匿名挂载**
```
# 1、指定路径挂载
# 指定路径挂载主要是在启动容器时使用 "-v" 参数，即 volume ， 
# 格式： docker run -v 宿主机内要挂载的路径:容器内要挂载的路径 镜像名或id
docker run -it -v /home/dsc/test:/home centos /bin/bash
    # 将宿主机内的 /home/dsc/test 挂载到容器内的  /home ，两者共享数据，只要有一个路径存在，就会同步数据。

# 可以挂载多个目录
docker run -it -v /home/dsc/test:/home centos -v /home/dsc/name:/username centos /bin/bash

# 2、匿名挂载 ，即在挂载时只指定容器内的目录，不指定宿主机的目录和挂载名称，系统会随机定义挂载名。
# 默认挂载到宿主机的 /var/lib/docker/volumes/随机生成的挂载名/_data
docker run -it -v /home centos /bin/bash
    将容器内的 /home 匿名挂载到宿主机的 /var/lib/docker/volumes/随机生成的挂载名/_data 。
    但是我的 Windows11 中下载的 ubuntu 没有这个路径，只有 /var/lib/docker-desktop ，未解决。

# 3、具名挂载 ，即在挂载时指定宿主机内的挂载名称，方便查找。
# 默认挂载到宿主机的 /var/lib/docker/volumes/设置的挂载名/_data
docker run -it -v juming_centos:/home centos /bin/bash
    将容器内的 /home 匿名挂载到宿主机的 /var/lib/docker/volumes/juming_centos/_data 。
```

### （3.3）**DockerFile 的使用**
DockerFile 是生成镜像的脚本，按照脚本的配置构建镜像。

有如下名为 dockerfile01 的脚本
```
FROM centos     # 从 centos 镜像生成
VOLUME ["volume01","volume02"] # 匿名挂载两个目录到宿主机
CMD echo "----end----" # 输出内容
CMD /bin/bash # 设置启动的控制台
```

**docker build 命令生成镜像**
```
# 进入 dockerfile01 所在目录，执行
docker build -f dockerfile01 -t centos_dsc:v1.0 .  # 最后的 "." 不要忘记
    -f filepath ，指定要从哪个 DockerFile 文件生成镜像。
    -t tag ，给镜像打标签，还可注明版本。
```
**数据卷容器**
```
# --volumes-from 可以继承现有容器的数据卷
# 格式： docker run -it --name="新容器名" --volumes-from 要继承的容器名或id 要运行的镜像名或id 
docker run -it --name="centos02" --volumes-from centos01 centos
    上面一行的意思是运行 centos 镜像，生成 centos02 容器， centos02 继承 centos01 的数据卷， centos01 此时被称为数据卷容器。
    数据卷容器中之前被挂载的目录中的数据会在生成的容器中共享。    
# 可以运行多个容器，都继承自数据卷容器 centos01 , 可实现多容器之间的数据共享。
# 数据卷容器的生命持续到没有容器使用为止，只要其中一个容器在使用，数据就不会消失。
```

**DockerFile 指令**  
基础知识：
* 所有指令都是大写
* 从上到下顺序执行
* "#" 表示注释
* 每一条指令都会创建并提交一个新的镜像层。

指令：
```
FROM         # 指定基础镜像
MAINTAINER   # 指定维护者信息，通常是姓名和邮箱
RUN          # 镜像构建时需要运行的命令
ADD          # 复制一些文件文件，会自动解压
WORKDIR      # 设置当前工作目录
VOLUME       # 设置卷，挂载主机目录
EXPOSE       # 暴露端口。若不设置，需要运行时使用 -p 指定。
CMD          # 指定容器启动时要运行的命令，只有最后一个会生效，可被替代
ENTRYPOINT   # 指定容器启动时要运行的命令，可以追加命令 
COPY         # 类似 ADD ，将文件拷贝到镜像中
ENV          # 构建镜像时设置环境变量
```

dockerfile 示例：
```
FROM centos
MAINTAINER DSC<2233429841@qq.com>
WORKDIR /home
VOLUME ["volume01","volume02"]
CMD echo "----end----"
```

### （3.4）**Docker 网络**

