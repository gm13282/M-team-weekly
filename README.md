## 使用步骤
### 1. 简介
因为每周都有一些免费资源在周末放出，有些朋友不能及时得到消息。为了方便大家及时收到提醒，我开发了这个小功能，当免费资源放出后，会通过ntfy进行通知。默认检查数据频率是1小时一次
### 2. 基础设施
一个安装有docker且可上网的机器即可。如果需要安装docker请访问这里 https://docs.docker.com/engine/install/
### 3. 下载docker-compose.yml文件
下载docker-compose.yml文件到服务器，以Ubuntu为例，比如/home/M-team目录，或者粘贴下面命令完成。
**注意** 请务必修改里面compose文件里面的内容
必须要修改的内容如下：
- API_KEY，登录你的账号-控制台-实验室-存取令牌生成
- AUTH_USERNAME，你的ntfy账号
- AUTH_PASSWORD，你的ntfy密码
- NOTIFICATION_TOPIC，你的ntfy设置的频道
其他内容默认也可以使用
```shell
sudo mkdir -p /home/M-team
```
```shell
cat <<EOF > /home/M-team/docker-compose.yml
services:
  M-team-notifier:
    image: ghcr.io/gm13282/m-team-weekly:main
    container_name: M-team-notifier
    environment:
      API_URL: "https://kp.m-team.cc/api/torrent/search"
      API_KEY: "Your_API_Key"
      MODE: "adult" # You can change to other categories
      PAGE_NUMBER: 1
      PAGE_SIZE: 25
      CHECK_INTERVAL: 3600 # update per hour
      AUTH_USERNAME: "name@email.com" # ntfy.sh user
      AUTH_PASSWORD: "password" # ntfy.sh password
      NOTIFICATION_URL: "https://ntfy.sh/" 
      NOTIFICATION_TOPIC: "my_topic" # ntfy.sh topic
      NOTIFICATION_TITLE: "Name your title" # name your title
      NOTIFICATION_PRIORITY: 3 # If you don't know how to modify it, please keep the 3
      NOTIFICATION_ACTIONS: '[{"action": "view", "label": "点击查看", "url": "https://www.google.com"}]'
      MESSAGE_MODE: 1 # If 1 will message the topic's name, 0 just "活動置頂"
EOF
```
### 启动服务
进入到/home/M-team目录，启动服务即可。
```shell
cd /home/M-team
sudo docker compose up -d
```
