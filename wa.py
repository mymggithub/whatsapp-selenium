#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import base64
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
import logging
logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s',filename='logging.txt',filemode='w')


class whatsapp():
	def __init__(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		chrome_path = dir_path + r"/chromedriver.exe"
		options = webdriver.ChromeOptions()
		options.add_argument('--ignore-certificate-errors')
		options.add_argument('--ignore-ssl-errors')
		os.environ["webdriver.chrome.driver"] = chrome_path
		self.driver = webdriver.Chrome(chrome_options=options, executable_path=chrome_path)
		self.wadriver = webdriver.Chrome(chrome_options=options, executable_path=chrome_path)
		self.open_url()

	def open_url(self):
		self.driver.get("https://translate.google.com/")
		self.wadriver.get("https://web.whatsapp.com/")

	def translate(self, word):
		blank = 0
		elem = self.driver.find_element_by_xpath("""//*[@id="source"]""")
		elem.clear()
		elem.send_keys("")
		time.sleep(1.5)
		elem.send_keys(word)
		while blank < 3:
			# time.sleep(1.5)
			try:
				ui.WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="result_box"]/span""")))
				result = self.driver.find_element_by_xpath("""//*[@id="result_box"]/span""")
				blank = 0
			except Exception as e:
				result = self.driver.find_element_by_xpath("""//*[@id="gt-res-error"]""")
				blank += 1
			if blank == 0:
				break
		return result.text

	def save_img(self, data):
		_, b64data = data.split(',')
		data = base64.decodestring(b64data)
		with open('data/picture_out.png', 'wb') as f:
			f.write(data)

	def auth_pic(self):
		repeat = 1
		while repeat:
			print("making another pic")
			time.sleep(1.5)
			try:
				ui.WebDriverWait(self.wadriver, 1).until(EC.visibility_of_element_located((By.XPATH, """//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div/img""")))
				img = self.wadriver.find_element_by_xpath("""//*[@id="app"]/div/div/div[2]/div[1]/div[2]/div/img""")
				data = img.get_attribute("src")
				self.save_img(data)
				background = Image.open("data/picture_out.png")
				foreground = Image.open("data/merge_with.png")
				old_im = Image.alpha_composite(background, foreground)# .save("login_pic.png")# .convert('1', dither=Image.NONE)
				old_size = old_im.size
				new_size = (400, 400)
				new_im = Image.new("RGB", new_size, (255, 255, 255))
				new_im.paste(old_im, ((new_size[0]-old_size[0])/2,(new_size[1]-old_size[1])/2))
				new_im.save('login_pic.png')
				repeat = 1
			except Exception as e:
				print(e)
				repeat = 0

	def find_user(self):
		user = self.wadriver.find_element_by_xpath('//span[@title = "{}"]'.format("Aunt Silvia"))
		user.click()

	def dropdown_menu(self):
		wadriver = self.wadriver
		ui.WebDriverWait(wadriver, 1).until(EC.visibility_of_element_located((By.XPATH, """(//*[contains(@data-pre-plain-text,' Aunt Silvia: ')])[last()]""")))
		element_to_hover_over = wadriver.find_element_by_xpath("""(//*[contains(@data-pre-plain-text,' Aunt Silvia: ')])[last()]""")
		hover = ActionChains(wadriver).move_to_element(element_to_hover_over)
		hover.perform()
		ui.WebDriverWait(wadriver, 1).until(EC.visibility_of_element_located((By.XPATH, '(//*[@data-icon="down-context"])[last()]')))
		dropdown = wadriver.find_element_by_xpath('(//*[@data-icon="down-context"])[last()]')
		dropdown.click()

	def click_reply(self):
		ui.WebDriverWait(self.wadriver, 1).until(EC.visibility_of_element_located((By.XPATH, '(//*[@title="Reply"])[last()]')))
		reply = self.wadriver.find_element_by_xpath('(//*[@title="Reply"])[last()]')
		reply.click()

	def send_msg(self, m):
		msg_box = self.wadriver.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
		msg_box.send_keys(m)
		msg_box.send_keys(Keys.RETURN)

	def check_msgs(self):
		lastMsg = ""
		while True:
			time.sleep(1.5)
			msg = self.wadriver.find_element_by_xpath("""(//*[contains(@data-pre-plain-text,' Aunt Silvia: ')])[last()]""").text
			if msg != lastMsg:
				tmsg = self.translate(msg)
				if msg != tmsg:
					self.dropdown_menu()
					self.click_reply()
					self.send_msg(tmsg)
					lastMsg = msg


if __name__ == "__main__":
	obj = whatsapp()
	print(obj.translate("Hola"))
	obj.auth_pic()
	obj.find_user()
	obj.check_msgs()

# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()

