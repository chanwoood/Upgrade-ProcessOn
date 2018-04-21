import random
import re
import time
import argparse

import requests

parser = argparse.ArgumentParser()
parser.add_argument('url')
args = parser.parse_args()
url = args.url

def getuser():

	user = str(random.randint(1000000, 9999999))
	
	return user

def getdomain():

	domains = [
		"@carbtc.net",
		"@2ether.net",
		"@eth2btc.info",
		"@web2mailco.com",
		"@1webmail.info",
		"@mailtrix.net",
		"@twocowmail.net",
		"@one2mail.info",
		"@uemail99.com",
		"@emailure.net",
		"@emailsy.info",
	]
	
	domain = random.choice(domains)
	
	return domain
	
	
def po(user, domain, url):

	ss_po = requests.Session()
	ss_po.get(url)

	fullname = str(random.randint(1000000, 9999999))
	password = str(random.randint(1000000, 9999999))

	

	processon = {
		'email': user + domain,
		'pass': password,
		'fullname': fullname
	}

	rsp_po = ss_po.post('https://www.processon.com/signup/submit', data=processon)

	fmt = "\nemail: {}\npassword: {}\nnickname: {}\n"
	print(fmt.format(processon.get('email'), password, fullname))


def mail(user, domain):

	ss_mail = requests.Session()
	rsp_get = ss_mail.get('https://temp-mail.org/zh/option/change/')
	csrf = re.findall(r'name="csrf" value="(\w+)', rsp_get.text)[0]

	tempmail = {
		'csrf': csrf,
		'mail': user,
		'domain': domain
	}

	ss_mail.post('https://temp-mail.org/zh/option/change/', data=tempmail)
		
	rsp_refresh = ss_mail.get('https://temp-mail.org/zh/option/refresh/')
	url_box = re.findall(r'https://temp-mail.org/zh/view/\w+', rsp_refresh.text)
	while url_box == []:
		time.sleep(1)
		rsp_refresh = ss_mail.get('https://temp-mail.org/zh/option/refresh/')
		url_box = re.findall(r'https://temp-mail.org/zh/view/\w+', rsp_refresh.text)
		
	rsp_message = ss_mail.get(url_box[0])
	url_verify = re.findall(r'https://www.processon.com/signup/verification/\w+', rsp_message.text)[0]
	rsp_verify = ss_mail.get(url_verify)
	
	global num
	
	if rsp_verify.status_code == 200:
		num += 1
		print('Number of successes：{}'.format(num))
		
num = 0

if __name__ == "__main__":
	
	while True:
		user = getuser()
		domain = getdomain()
		
		po(user, domain, url)
		mail(user, domain)
	
