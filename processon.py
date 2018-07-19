from concurrent.futures import ThreadPoolExecutor
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from captcha import Crack



domains = []
count = 0


def getuser():

    user = str(random.randint(1000000, 9999999))

    return user


def getdomain():
    global domains
    if domains == []:
        r = requests.get("https://temp-mail.org/en/option/change/")
        soup = BeautifulSoup(r.text, "html.parser")
        domains = [tag.text for tag in soup.find(id="domain").find_all("option")]
    return random.choice(domains)


def po(user, domain, url):
    fullname = str(random.randint(1000000, 9999999))
    password = str(random.randint(1000000, 9999999))
    # url, email, psw, name
    crack = Crack(url, user + domain, password, fullname)
    crack.open()

    fmt = "\nemail: {}"
    print(fmt.format(user + domain))


def mail(user, domain):
    global count

    ss_mail = requests.Session()
    rsp_get = ss_mail.get("https://temp-mail.org/zh/option/change/")
    csrf = re.findall(r'name="csrf" value="(\w+)', rsp_get.text)[0]

    tempmail = {"csrf": csrf, "mail": user, "domain": domain}

    ss_mail.post("https://temp-mail.org/zh/option/change/", data=tempmail)

    rsp_refresh = ss_mail.get("https://temp-mail.org/zh/option/refresh/")
    url_box = re.findall(r"https://temp-mail.org/zh/view/\w+", rsp_refresh.text)
    while url_box == []:
        time.sleep(1)
        rsp_refresh = ss_mail.get("https://temp-mail.org/zh/option/refresh/")
        url_box = re.findall(r"https://temp-mail.org/zh/view/\w+", rsp_refresh.text)

    rsp_message = ss_mail.get(url_box[0])
    url_verify = re.findall(
        r"https://www.processon.com/signup/verification/\w+", rsp_message.text
    )
    rsp_verify = ss_mail.get(url_verify[0])

    if rsp_verify.status_code == 200:
        count += 1
        print("{}@{} 成功! 【共成功{}次】".format(user, domain, count))


def make(user):
    domain = getdomain()
    po(user, domain, url)
    mail(user, domain)


if __name__ == "__main__":
    # url = "https://www.processon.com/i/5ad16f4be4b0518eacae31fb"
    url = input("请输入你的邀请链接：")
    for i in range(100):
        make(getuser())