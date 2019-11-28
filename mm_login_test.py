import unittest
import datetime
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

link="https://docs.google.com/spreadsheets/d/1YzP8PrQ_wncYIRF5d45BlmCIe_-1oIKQpdNDjFiZNhI/edit#gid=0"

class MattermostSeleniumTest(unittest.TestCase):

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

        def login(self,email,password):
            self.driver.find_element_by_name('loginId').send_keys(email)
            self.driver.find_element_by_name('password').send_keys(password)
            self.driver.find_element_by_id('loginButton').click()
            sleep(10)

        def logout(self):
            sleep(3)
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
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            date = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
            name = 'test-sel1-' + date
            assert "Submission Created." == self.postmessage('/messages/@jarvisbot', 'create-submission ' + name + " " + date + " 2 " + link)

        def test_use_case_1_sad(self):
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            name = 'test-sel1'
            date = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
            assert """Error invalid parameters. Usage: create-submission <name> 
                                         <Deadline YYYY/MM/DD-HH:MM> <# issues> <Submission Link>""" == self.postmessage('/messages/@jarvisbot', 'create-submission '+ name + " " + date + link)

        def test_use_case_1_sad_2(self):
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            date = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
            name = 'test-sel1-' + date
            assert "Submission Created." == self.postmessage('/messages/@jarvisbot',
                                                           'create-submission ' + name + " " + date + " 2 "+link)
            assert "Name already exists. Please provide a new Name." == self.postmessage('/messages/@jarvisbot', 'create-submission ' + name + " " + date + " 2 "+link)

        def test_use_case_1_sad_3(self):
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            date = datetime.datetime.now().strftime("%Y/%m/%d-%H:%M")
            wrong_date = datetime.datetime.now().strftime("%Y/%m/%d")
            name = 'test-sel1-' + date
            assert "Incorrect date format, should be YYYY/MM/DD-HH:MM." == self.postmessage('/messages/@jarvisbot',
                                                         'create-submission ' + name + " " + wrong_date + " 2 "+link)

        def test_use_case_3_happy(self):
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            date = datetime.datetime.now() + datetime.timedelta(minutes=5)
            date = date.strftime("%Y/%m/%d-%H:%M")
            name = 'test-sel3-' + date
            assert "Submission Created." == self.postmessage('/messages/@jarvisbot',
                                                             'create-submission ' + name + " " + date + " 2 "+link)
            assert "Keywords added." == self.postmessage('/messages/@jarvisbot','add-keywords ' + name + ' graphql,postgres')
            self.logout()
            sleep(10)
            self.login("test@ncsu.edu","Jarvisbot@2019")
            self.postmessage('/channels/questions', "where is graphql used in the industry?")
            sleep(10)
            assert "You received a Good Question Reward for posting a relevant question" == self.postmessage('/messages/@jarvisbot')
            self.logout()

        def test_use_case_3_sad(self):
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            date = datetime.datetime.now() - datetime.timedelta(minutes=5)
            date = date.strftime("%Y/%m/%d-%H:%M")
            name = 'test-sel3-' + date
            assert "Submission Created." == self.postmessage('/messages/@jarvisbot',
                                                            'create-submission ' + name + " " + date + " 2 "+link )
            assert "Keywords added." == self.postmessage('/messages/@jarvisbot',
                                                        'add-keywords ' + name + ' puppeteer')
            self.logout()
            sleep(10)
            self.login("test@ncsu.edu","Jarvisbot@2019")
            self.postmessage('/messages/@jarvisbot', 'show-rewards')
            self.postmessage('/channels/questions', "where is mockito used in the industry?")
            sleep(10)
            assert "You received a Good Question Reward for posting a relevant question" != self.postmessage('/messages/@jarvisbot')
            self.logout()

        def test_use_case_3_sad_2(self):
            self.login("jsdeokar@ncsu.edu","Jarvisbot@2019")
            date = datetime.datetime.now() + datetime.timedelta(minutes=5)
            date = date.strftime("%Y/%m/%d-%H:%M")
            name = 'test-sel3-' + date
            assert "Submission Created." == self.postmessage('/messages/@jarvisbot',
                                                            'create-submission ' + name + " " + date + " 2 "+link)
            assert "Keywords added." == self.postmessage('/messages/@jarvisbot',
                                                        'add-keywords ' + name + ' mockito,puppeteer')
            self.logout()
            sleep(10)
            self.login("test@ncsu.edu","Jarvisbot@2019")
            self.postmessage('/messages/@jarvisbot', 'show-rewards')
            self.postmessage('/channels/questions', "What is the deadline?")
            sleep(10)
            assert "You received a Good Question Reward for posting a relevant question" != self.postmessage('/messages/@jarvisbot')
            self.logout()

        def tearDown(self):
            self.driver.close()
