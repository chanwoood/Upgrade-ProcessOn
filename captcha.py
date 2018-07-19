from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class Crack():
    def __init__(self, url, email, psw, name):
        self.url = url
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 100)
        self.email = email
        self.psw = psw
        self.name =name
        self.BORDER = 6

    def open(self):
        """
        打开浏览器,并输入注册信息
        """
        self.browser.get(self.url)
        btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
        btn.click()
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'login_email')))
        psw = self.wait.until(EC.presence_of_element_located((By.ID, 'login_password')))
        name = self.wait.until(EC.presence_of_element_located((By.ID, 'login_fullname')))
        btn = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'button')))
        email.send_keys(self.email)
        psw.send_keys(self.psw)
        name.send_keys(self.name)
        btn.click()
        self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'signup_box')))