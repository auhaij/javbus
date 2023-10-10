import requests, json, time, os, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from lxml import etree

cookie = "existmag=mag; 4fJN_2132_saltkey=VI4zzj5z; 4fJN_2132_lastvisit=1694928941; 4fJN_2132_lastcheckfeed=319004%7C1694932549; 4fJN_2132_nofavfid=1; 4fJN_2132_smile=4D1; 4fJN_2132_fastpostrefresh=1; 4fJN_2132_ulastactivity=5c3ftabU2WHjmH6n8rHUjhfmXi%2BIw9PCB0mreTuDHd2iykoLUazf; 4fJN_2132_auth=6d2abPEBOtYb28CxsG5NdQ7VX1uA0mafRQe0Ogz4zNnsl0peTGCjKFX2AgLSwlZTDCrkor3x%2F2tdxiP5n3%2FFtL973VU; PHPSESSID=kp6vfvmhe5h0tii5j7dnv4kgi6; 4fJN_2132_home_diymode=1; 4fJN_2132_st_p=319004%7C1696931335%7Ca7bcddcba61545a478da9826f5040054; 4fJN_2132_viewid=tid_109938; 4fJN_2132_visitedfid=2D36D37; 4fJN_2132_st_t=319004%7C1696931947%7Cd91f7f9c3248dec2764cac37ac0ad458; 4fJN_2132_forum_lastvisit=D_37_1696927476D_2_1696931947; 4fJN_2132_checkpm=1; 4fJN_2132_sid=o554V4; 4fJN_2132_lip=172.71.134.97%2C1696931947; 4fJN_2132_lastact=1696932619%09home.php%09misc; 4fJN_2132_sendmail=1"

def run(*arg):
    msg = ""
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'})

    # 签到
    url = "https://www.javbus.com/forum/home.php?mod=spacecp&ac=credit"
    headers = {
        'authority': 'www.javbus.com',
        'method': 'GET',
        'path': '/forum/home.php?mod=spacecp&ac=credit',
        'scheme': 'https',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        #'Connection' : 'keep-alive',
        #'Host' : 'www.right.com.cn',
        'Upgrade-Insecure-Requests' : '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language' : 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cookie': cookie,
        'referer': 'https://www.javbus.com/forum/home.php?mod=spacecp'
    }
    try:
        r = s.get(url, headers=headers, timeout=120)
        # print(r.text)
        if '每天登录' in r.text:
            h = etree.HTML(r.text)
            data = h.xpath('//tr/td[6]/text()')
            msg += f'签到成功或今日已签到，最后签到时间：{data[0]}'
        else:
            msg += '签到失败，可能是cookie失效了！'
            pusher(msg)
    except:
        msg = '无法正常连接到网站，请尝试改变网络环境，试下本地能不能跑脚本，或者换几个时间点执行脚本'
    return msg + '\n'

def main(*arg):
    msg = ""
    global cookie
    if "\\n" in cookie:
        clist = cookie.split("\\n")
    else:
        clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += run(cookie)
        i += 1
    print(msg[:-1])
    return msg[:-1]


if __name__ == "__main__":
    if cookie:
        print("----------巴士论坛开始尝试签到----------")
        main()
        print("----------巴士论坛签到执行完毕----------")
