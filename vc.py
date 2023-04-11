import requests, numpy, datetime, sys, configparser, json, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from bs4 import BeautifulSoup

def conf(s_name):
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
        list = {}
        for k,v in config.items(s_name):
            list.update({k: v})
        return list
    except:
        print('未找到config.ini配置文件,程序退出')
        sys.exit(0)

def VC():
    url = 'https://free.vps.vc/create-vps'
    cookie = conf('vc')['cookie']
    headers = {
        'authority': 'free.vps.vc',
        'method': 'GET',
        'path': '/create-vps',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': cookie,
        'referer': 'https://free.vps.vc/vps-info',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }

    resp = requests.get(url, headers=headers)
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
        print(f'当前时间:{datetime.datetime.now()} \n VC请求错误(网络请求频繁,正常情况,注意检查cookie填写是否正常)')
        return []

def checkVC():
    send('VC监控启动...')
    print('VC监控启动...')
    checkList = []
    dt = ""
    while(True):
        dc = VC()
        if len(dc) != 0:
            if dt == "":
                dt = datetime.datetime.now()
            if numpy.all(checkList == dc):
                pass
            else:
                str = '\n'.join(dc)
                send(f'VC库存发生变化 ==== 当前时间 {datetime.datetime.now()} \n {str}')
                print(f'VC库存发生变化 ==== 当前时间 {datetime.datetime.now()} \n {str}')
                checkList = dc
        else:
            nullList = []
            if numpy.all(checkList != nullList):
                send(f'VC库存已抢完! ==== 当前时间 {datetime.datetime.now()}')
                print(f'VC库存已抢完! ==== 当前时间 {datetime.datetime.now()}')
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

if __name__ == '__main__':
    checkVC()