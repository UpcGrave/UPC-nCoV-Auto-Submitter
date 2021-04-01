# coding=utf-8
import requests, time, json, configparser, random, os, yagmail
from utils.serverchan_push import push_to_wechat



## serverchan
SERVERCHAN_SECRETKEY = "replace to your key"
## [SMTP]
SMTP_user = "replace to your info"
SMTP_password = "replace to your info"
SMTP_host = "replace to your info"


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

# 获取当前的时间
def get_time():
    return time.strftime('%Y%m%d', time.localtime(time.time()))


# 帐号密码信息读取,密码采用加密方式传输
def getUserInfo():
    try:
        config = configparser.ConfigParser()
        config.read('/home/wukang/auto_covid19/info.ini')
        usernames = config['Information']['username'].split(',')
        passwords = config['Information']['password'].split(',')
        emails = config['Information']['email'].split(',')
        
        print('get userdata success')
        return list(zip(usernames, passwords, emails))

    except Exception as e:
        print('get userdata failed\n %s' % e)
        return None


def login(userdata):
    login_url = "https://app.upc.edu.cn/uc/wap/login/check"
    session = requests.session()
    response = session.post(login_url, headers=headers, data=userdata, timeout=20)
    response.encoding = "UTF-8"
    print(response.text,'\n')
    info_url = "https://app.upc.edu.cn/ncov/wap/default/index"
    html_info = session.get(info_url, headers=headers,timeout=20)
    html_info.encoding = "UTF-8"
    return session, html_info.text


def save_info(session, info):
    save_url = "https://app.upc.edu.cn/ncov/wap/default/save"
    save_response = session.post(url=save_url,data=info,headers=headers,timeout=20)
    save_response.encoding = "UTF-8"
    return save_response.text

def send_email(status, info, email_address):
    yagmail_server = yagmail.SMTP(user=SMTP_user, password=SMTP_password, host=SMTP_host)
    email_name = [email_address]
    email_title = [status]
    email_content = [info]
    yagmail_server.send(to=email_name, subject=email_title, contents=email_content)
    yagmail_server.close()
    print("email finished")


def process(userdata, email_address):
    # 登录返回old_info
    session, html = login(userdata)
    print(html)
    old_info = json.loads(html)['d']['oldInfo']

    # 获取当前日期
    today_date = get_time()

    # 重构old_info
    old_info['date'] = today_date
    print(old_info)

    # 提交信息，对应的接口为save
    save_res = save_info(session,old_info)
    print(save_res)
    session.close()

    # 结束后发送邮件
    if json.loads(save_res)['m'] == '操作成功':
        is_fail = 0 
        #send_email("[success] covid-19 submission",str(json.loads(save_res)) + '\n' + str(old_info), email_address)
        pass
    else :
        is_fail = 1
        send_email("[failed] covid-19 submission", str(json.loads(save_res)) + '\n' + str(old_info), email_address)
        pass
    return save_res, is_fail

if __name__ == "__main__":
    # 获取用户信息
    userinfos = getUserInfo()
    print(userinfos)
    #userinfos = [userinfos[1]]
    res = []
    fail_cnt = 0
    for user in userinfos:
        print(user)
        try:
            user_data = {
                'username': user[0],
                'password': user[1]
            }
            print(user_data)
            info, is_fail = process(user_data, user[2])
            res.append({
                'username' : user[0],
                'info' : info
            })
            fail_cnt = fail_cnt + is_fail
        except Exception as e:
            print(e)
            fail_cnt = fail_cnt + 1
            res.append({
                'username' : user[0],
                'info' : e
            })
    # process(userdata, email_address)
    if fail_cnt == 0:
        res_text = "成功！！！疫情防控每日签到"
    else:
        res_text = "失败！！！疫情防控每日签到"
    push_to_wechat(text = res_text,
                    desp = str(res),
                    secretKey = SERVERCHAN_SECRETKEY)



