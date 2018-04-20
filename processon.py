import random
import re
import time
import requests

user = str(random.randint(1000000, 9999999))


ss = requests.Session()
rr = ss.get('https://www.processon.com/i/5ad16f4be4b0518eacae31fb')


processon = {
	'email': user + '@carbtc.net',
	'pass': str(random.randint(1000000, 9999999)),
	'fullname': str(random.randint(1000000, 9999999))
}

rsp_po = ss.post('https://www.processon.com/signup/submit', data=processon)

print("register code: {}\nuser: {}".format(rsp_po.status_code, user))


s = requests.Session()
rsp_g = s.get('https://temp-mail.org/zh/option/change/')
csrf = re.findall(r'name="csrf" value="(\w+)', rsp_g.text)[0]

data = {
	'csrf': csrf,
	'mail': user,
	'domain': '@carbtc.net'
}

rsp_p = s.post('https://temp-mail.org/zh/option/change/', data=data)
if rsp_p.status_code == 200:
	print('email: {}@carbtc.net'.format(user))
else:
	print('change email false')
	
rsp_refresh = s.get('https://temp-mail.org/zh/option/refresh/')
url_box = re.findall(r'https://temp-mail.org/zh/view/\w+', rsp_refresh.text)
while url_box == []:
	time.sleep(1)
	rsp_refresh = s.get('https://temp-mail.org/zh/option/refresh/')
	url_box = re.findall(r'https://temp-mail.org/zh/view/\w+', rsp_refresh.text)
	
rsp_message = s.get(url_box[0])

url = re.findall(r'https://www.processon.com/signup/verification/\w+', rsp_message.text)[0]
r = s.get(url)
print('verification url status code: {}'.format(r.status_code))
