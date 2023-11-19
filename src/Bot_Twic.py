import json
import os
from time import sleep
from itertools import cycle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from fake_useragent import UserAgent
import undetected_chromedriver as uc
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading
driver_lock = threading.Lock()

class GoogleBot:
    def __init__(self, profile, proxy, option, use_proxy=True):
        self.profile = profile
        self.proxy = proxy if use_proxy else None
        self.option = option
        self.use_proxy = use_proxy
        self.json_file_path = os.path.join("data", "comments.json")
        self.comments = self.load_comments_from_json()
        self.initialize_driver()

    def load_proxy_list(self):
        proxy_file_path = os.path.join("data", "Proxy.txt")
        with open(proxy_file_path, 'r') as file:
            return [line.strip() for line in file]

    def initialize_driver(self):
        global driver_lock
        with driver_lock:
            options = uc.ChromeOptions()
            if self.use_proxy and self.proxy:
                options.add_argument(f'--proxy-server={self.proxy}')
            options.add_argument(f"--user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data\\{self.profile}")
            if self.option == "--headless":
                options.add_argument("--headless")
            options.add_argument("--incognito")
            self.driver = uc.Chrome(options=options)
    def open_url(self, url):
        try:
            sleep(1)
            self.driver.get(url)
            cookie = self.set_x_main()
            sleep(2)
            self.driver.add_cookie(cookie)
            self.driver.refresh()
        except Exception as e:
            print(f"Error in open_url: {e}")

    def set_x_main(self):
        cookie = {"name": "auth-token", "value": "k4jjqecvjshhm0hk20spjvlbpq0vpx"}
        return cookie
    def load_comments_from_json(self):
        # قراءة الملف JSON وتحميل البيانات
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return [item['comment'] for item in data]  # استخراج النصوص فقط
    def send_chat_message(self, message):
        try:
            wait = WebDriverWait(self.driver, 20)  # الانتظار لمدة 10 ثواني كحد أقصى
            chat_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-a-target="chat-input"]')))
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print("عنصر إدخال الدردشة غير موجود.")
        except Exception as e:
            print(f"حدث خطأ أثناء إرسال الرسالة: {e}")
    def start(self):
        try:
            url = "https://www.twitch.tv/jskillz_lol"
            self.open_url(url)
            for comment in cycle(self.comments):  # تكرار على التعليقات بشكل دوري
                self.send_chat_message(comment)
                sleep(120)  # الانتظار لمدة دقيقتين قبل الرسالة التالية
        except Exception as e:
            print(f"An error occurred in start method: {e}")

