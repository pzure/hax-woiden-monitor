import requests, threading, numpy, datetime, signal, sys, configparser, json, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from bs4 import BeautifulSoup

def conf(s_name):
    config = configparser.ConfigParser()
    try:
        config.read('config.ini', encoding='utf-8')
        list = {}
        for k,v in config.items(s_name):
            list.update({k: v})
        return list
    except Exception as e:
        print('未找到config.ini配置文件,程序退出!',e)
        sys.exit(0)

def Hax():
    url = "https://hax.co.id/create-vps/"
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
    resp = requests.get(url=url, headers=headers)
    html_content = resp.content.decode('UTF-8')

    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        el = soup.find(id = "datacenter")
        option = el.find_all('option')
        res = []
        for i in option:
            if i.text != '-select-':
                res.append(i.text)
        return res
    except:
        print(f'当前时间{datetime.datetime.now()} ==== Hax请求错误')
        return []
def Woiden():
    url = "https://woiden.id/create-vps/"
    headers = {
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    }
    resp = requests.get(url=url, headers=headers)
    html_content = resp.content.decode('UTF-8')

    soup = BeautifulSoup(html_content, 'html.parser')
    try:
        el = soup.find(id = "datacenter")
        option = el.find_all('option')
        res = []
        for i in option:
            if i.text != '-select-':
                res.append(i.text)
        return res
    except:
        print(f'当前时间:{datetime.datetime.now()} \n Woiden请求错误(网络请求频繁,正常情况)')
        return []
def checkHax():
    send('Hax监控启动...')
    print('Hax监控启动...')
    checkList = []
    dt = ""
    while(True):
        dc = Hax()
        if len(dc) != 0:
            if dt == "":
                dt = datetime.datetime.now()
            if numpy.all(checkList == dc):
                pass
            else:
                str = '\n'.join(dc)
                send(f'Hax库存发生变化 ==== 当前时间 {datetime.datetime.now()} \n {str}')
                print(f'Hax库存发生变化 ==== 当前时间 {datetime.datetime.now()} \n {str}')
                checkList = dc
        else:
            nullList = []
            if numpy.all(checkList != nullList):
                send(f'Hax库存已抢完! ==== 当前时间 {datetime.datetime.now()}')
                print(f'Hax库存已抢完! ==== 当前时间 {datetime.datetime.now()}')
                checkList = []
                if dt != "":
                    dt = ""
def checkWoiden():
    send('Woiden监控启动...')
    print('Woiden监控启动...')
    checkList = []
    dt = ""
    while(True):
        dc = Woiden()
        if len(dc) != 0:
            if dt == "":
                dt = datetime.datetime.now()
            if numpy.all(checkList == dc):
                pass
            else:
                str = '\n'.join(dc)
                send(f'Woiden库存发生变化 ==== 当前时间 {datetime.datetime.now()} \n {str}')
                print(f'Woiden库存发生变化 ==== 当前时间 {datetime.datetime.now()} \n {str}')
                checkList = dc
        else:
            nullList = []
            if numpy.all(checkList != nullList):
                send(f'Woiden库存已抢完! ==== 当前时间 {datetime.datetime.now()}')
                print(f'Woiden库存已抢完! ==== 当前时间 {datetime.datetime.now()}')
                checkList = []
                if dt != "":
                    dt = ""

def tg(msg):
    item = conf('tgbot_info')
    bot_token = item['tgbot_token']
    global chat_ids
    url = f"https://api.telegram.org/bot{bot_token}"
    try:
        response = requests.get(f'{url}/getUpdates?offset=0&limit=100')
        res_data = json.loads(response.text)
        updates = res_data["result"]
        for update in updates:
            if "message" in update:
                chat_ids.append(update["message"]["chat"]["id"])
            elif "my_chat_member" in update:
                chat_ids.append(update["my_chat_member"]["chat"]["id"])
            else:
                print('用户查找异常')
        for chat_id in list(set(chat_ids)):
            data = {
                'chat_id' : chat_id,
                'text': msg
            }
            resp = requests.post(f"{url}/sendMessage", data=data)
            print(resp.json())
    except:
        print('bot接口请求失败')
def mail(msg):
    ei = conf('email_info')
    for r_email in ei['receiver_email'].split(','):
        message = MIMEText(msg, 'plain', 'utf-8')
        message['From'] = formataddr(('AUXBot', ei['sender_email']))
        message['To'] = formataddr(('告警用户',r_email))
        # message['Subject'] = ei['subject']
        try:
            message['Subject'] = msg.split('\n')[0]
        except:
            message['Subject'] = msg
        try:
            server = smtplib.SMTP_SSL(ei['smtp_server'], 465)
            server.login(ei['sender_email'], ei['sender_password'])
            server.sendmail(ei['sender_email'], r_email, message.as_string())
            server.quit()
            print('发送成功')
        except Exception as e:
            print(f'发送失败,错误信息{e}')
chat_ids = []
def send(msg):
    opt = conf('options')
    if opt['tgbot'] == '1' and opt['email'] == '0':
        tg(msg)
    elif opt['tgbot'] == '0' and opt['email'] == '1':
        mail(msg)
    elif opt['tgbot'] == '1' and opt['email'] == '1':
        tg(msg)
        mail(msg)
    else:
        print('未启用发送媒介')
# 正常结束进程
def signal_handler(sig, frame):
    lock = threading.Lock()
    with lock:
        print("程序已结束")
        sys.exit(0)
# 多线程
def thread_check(signal_handler):
    signal.signal(signal.SIGINT, signal_handler)
    t1 = threading.Thread(target=checkHax)
    t2 = threading.Thread(target=checkWoiden)
    t1.start()
    t2.start()

if __name__ == '__main__':
    thread_check(signal_handler)

'''
后台运行记录日志命令
nohup python3 -u hax-woiden.py > bot.log 2>&1 &
'''