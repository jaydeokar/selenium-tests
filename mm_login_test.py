import unittest
import datetime
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class GithubWatchRepoTest(unittest.TestCase):

        def setUp(self):
            self.teamname = "csc-510-f19"
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_argument("--no-sandbox")
            chromeOptions.add_argument("--disable-setuid-sandbox")
            chromeOptions.add_argument("--disable-dev-shm-using")
            chromeOptions.add_argument("--disable-extensions")
            chromeOptions.add_argument("--disable-gpu")
            chromeOptions.add_argument("start-maximized")
            chromeOptions.add_argument("disable-infobars")
            chromeOptions.add_argument("--headless")
            self.driver = webdriver.Chrome(chrome_options=chromeOptions, executable_path="/usr/bin/chromedriver")
            self.url = "http://34.66.232.72:8065/"
            self.driver.get(self.url)
            sleep(10)

        def login(self):
            self.driver.find_element_by_name('loginId').send_keys("jsdeokar@ncsu.edu")
            self.driver.find_element_by_name('password').send_keys("Jarvisbot@2019")
            self.driver.find_element_by_id('loginButton').click()
            sleep(10)

        def logout(self):
            self.driver.find_element_by_id('headerInfo').click()
            self.driver.find_element_by_id('logout').click()
            sleep(2)

        def postmessage(self, channel, msg=None):
            postchannel = self.url + self.teamname + channel
            self.driver.get(postchannel)
            sleep(10)
            if msg:
                element = self.driver.find_element_by_id('post_textbox')
                element.send_keys(msg)
                element.submit()
                sleep(10)
            a = self.driver.find_elements_by_class_name("post-message__text")
            return a[-1].text

        def test_use_case_1_happy(self):
            self.login()
            date = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
            name = 'test-sel1-' + date
            assert "Submission Created." == self.postmessage('/messages/@jarvisbot','create-submission ' + name + "https://docs.google.com/spreadsheets/")

        def test_use_case_1_sad(self):
            self.login()
            name = 'test-sel1'
            date = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
            assert """Error invalid parameters. Usage: create-submission <name> 
                                         <Deadline YYYY/MM/DD-HH:MM> <# issues> <Submission Link>""" == self.postmessage(
            '/messages/@jarvisbot', 'create-submission '
                                    + name + " " + date + link)

        def tearDown(self):
            self.driver.close()
