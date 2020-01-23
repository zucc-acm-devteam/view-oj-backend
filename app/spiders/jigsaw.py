import platform
import random
import time
from io import BytesIO

import cv2
import numpy as np
import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Jigsaw:
    def __init__(self, url: str,
                 bg_image_class: str = 'yidun_bg-img',
                 fullbg_image_class: str = 'yidun_jigsaw',
                 button_class: str = 'yidun_slider',
                 headless: bool = False,
                 timeout: int = 5):
        self.timeout: int = timeout
        self.url: str = url
        self.bg_image_class = bg_image_class
        self.fullbg_image_class = fullbg_image_class
        self.button_class = button_class
        self.driver: webdriver = self.create_driver(headless)
        self.WAIT: WebDriverWait = WebDriverWait(self.driver, self.timeout)

    def run(self):
        bg_image = self.get_images(self.bg_image_class)
        fullbg_image = self.get_images(self.fullbg_image_class)
        print('get image successful')
        distance = self.get_distance(bg_image, fullbg_image)
        print('calculate distance successful', distance)
        track = self.get_track(distance)
        self.drag_the_ball(track)
        print('drag the ball successful')

    def create_driver(self, headless: bool):
        options = webdriver.ChromeOptions()
        options.add_argument("log-level=3")
        if headless:
            options.add_argument("headless")
        else:
            options.add_argument("disable-infobars")
            options.add_argument("window-size=1200,1200")
        if platform.system() == "Linux":
            options.add_argument("no-sandbox")
            from pyvirtualdisplay import Display

            display = Display(visible=0, size=(1200, 120))
            display.start()
        driver = webdriver.Chrome(options=options)
        driver.get(self.url)
        return driver

    def get_images(self, class_: str):
        self.WAIT.until(EC.element_to_be_clickable((By.CLASS_NAME, self.button_class)))
        time.sleep(2)
        bs = BeautifulSoup(self.driver.page_source, 'lxml')
        # 找到背景图片和缺口图片的div
        img_div = bs.find_all(class_=class_)
        # 获取缺口背景图片url
        img_url = img_div[0].attrs['src']
        # 下载图片
        image = requests.get(img_url).content
        # 写入图片
        image_file = BytesIO(image)
        return Image.open(image_file)

    @staticmethod
    def get_distance(bg_image: Image, fullbg_image: Image):
        img_gray = cv2.cvtColor(np.asarray(bg_image), cv2.COLOR_RGB2BGR)
        img_gray = cv2.cvtColor(img_gray, cv2.COLOR_BGR2GRAY)
        template = cv2.cvtColor(np.asarray(fullbg_image), cv2.COLOR_RGB2BGR)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        run = 1

        # 使用二分法查找阈值的精确值
        L = 0
        R = 1
        while run < 20:
            run += 1
            threshold = (R + L) / 2
            if threshold < 0:
                print('Error')
                return None
            loc = np.where(res >= threshold)
            if len(loc[1]) > 1:
                L += (R - L) / 2
            elif len(loc[1]) == 1:
                return loc[1][0] + 3
            elif len(loc[1]) < 1:
                R -= (R - L) / 2

    @staticmethod
    def get_track(distance: int, type_=1):
        if type_ == 1:
            return [distance]
        elif type_ == 2:
            track = []
            r = distance - 1
            while r:
                tmp = random.randint(-1, 10)
                if r > tmp:
                    track.append(tmp)
                    r -= tmp
                else:
                    track.append(r)
                    r = 0
            return track
        elif type_ == 3:
            track = []
            current = 0
            mid = distance * 3 / 4
            t = random.randint(2, 3) / 10
            v = 0
            while current < distance:
                if current < mid:
                    a = 2
                else:
                    a = -3
                v0 = v
                v = v0 + a * t
                move = v0 * t + 1 / 2 * a * t * t
                current += move
                track.append(round(move))
            return track
        else:
            raise Exception('type error')

    def drag_the_ball(self, track: list):
        knob = self.WAIT.until(
            EC.presence_of_element_located((By.CLASS_NAME, self.button_class)))
        ActionChains(self.driver).click_and_hold(knob).perform()
        while track:
            x = random.choice(track)
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=random.randint(-5, 5)).perform()
            track.remove(x)
        time.sleep(0.1)
        imitate = ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=random.randint(-5, 5))
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6, 10) / 10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        imitate.perform()
        time.sleep(0.033)
        ActionChains(self.driver).move_by_offset(xoffset=1, yoffset=random.randint(-5, 5)).perform()
        ActionChains(self.driver).pause(random.randint(6, 14) / 10).release(knob).perform()

    def get_cookies(self):
        return self.driver.get_cookies()

    def get_url(self):
        return self.driver.current_url

    def close(self):
        self.driver.close()
        self.driver.quit()

    def send_keys(self, value: str, xpath: str):
        self.WAIT.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = self.driver.find_element_by_xpath(xpath)
        element.clear()
        element.send_keys(value)

    def click(self, xpath: str):
        self.WAIT.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = self.driver.find_element_by_xpath(xpath)
        element.click()

    def url_to_be(self, url: str):
        self.WAIT.until(EC.url_to_be(url))
