# hax-woiden-monitor

hax监控基于Python3

##食用方法：

* 填写config.ini配置文件
  将需要启用的消息媒介值改为1

  ```ini
  [options]
  #需要使用的提醒方式将0改为1
  tgbot = 0
  email = 0
  ```
* 按文件提示填写消息媒介资料

  ```ini
  [email_info]
  #发件方邮箱
  sender_email =
  #密码或者key
  sender_password =
  #收件人信息,多个请用英文逗号隔开
  receiver_email =
  #smtp服务器,默认是QQ邮箱,如用其他邮箱请自行修改
  smtp_server =
  #邮件标题
  subject = 
  [tgbot_info]
  #telegram 机器人的key
  tgbot_token = 
  ```
* 安装支持包

  ```bash
  #进入到项目目录下执行
  pip3 install -r requirements.txt
  ```
* 启动监控

  ```bash
  #直接启动
  python3 hax-woiden.py
  #后台运行,记录日志(日志记录在当前目录的bot.log中)
  nohup python3 -u hax-woiden.py > bot.log 2>&1 &
  ```
* 使用VC监控

  ```ini
  #需要在浏览器先登录free.vps.vc 获取请求头中的cookie,填写到配置文件中
  [vc]
  #如果使用vc监控请填入网页中请求头的Cookie
  cookie =
  ```
* 启动VC监控

  ```bash
  #直接启动
  python3 vc.py
  #后台运行,记录日志(日志记录在当前目录的bot_vc.log中)
  nohup python3 -u hax-woiden.py > bot_vc.log 2>&1 &
  ```
