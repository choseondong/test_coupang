
from xml.dom.minidom import Element
from conftest import driver
from selenium.webdriver.common.by import By  # By 모듈 추가
#from config import EMAIL, PASSWORD

class LoginPage: 
  
  #user password and account info input function
  #coopang login page open
  #account input 찾기 -> xpath: //~~
  #password input ~~
  URL = "https://login.coupang.com"

  def __init__(self,driver):
    self.driver = driver

  def open(self):
    self.driver.get(self.URL)

  def input_password_and_email(self):
    input_email = self.driver.find_element(By.ID,"email").send_keys("cho951014@naver.com")
    input_password = self.driver.find_element(By.ID,"password").send_keys("005rkqkd")

  def click_login_button(self):
    login = self.driver.find_element(By.XPATH, "//button[text()='로그인']")
