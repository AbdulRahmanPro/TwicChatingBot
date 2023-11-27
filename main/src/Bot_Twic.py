import json
import os
from time import sleep
from itertools import cycle
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver as uc
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import shutil

driver_lock = threading.Lock()

class GoogleBot:
    def __init__(self, profile_id, proxy, option, use_proxy, token):
        self.profile_id = profile_id
        self.proxy = proxy if use_proxy else None
        self.option = option
        self.use_proxy = use_proxy
        self.username_proxy = "nwwugecc"  # تأكد من وضع القيم الصحيحة هنا
        self.password_proxy = "dn7pqelyht0s"  # تأكد من وضع القيم الصحيحة هنا
        self.json_file_path = os.path.join("data", "comments.json")
        self.comments = self.load_comments_from_json()
        self.token = token  # إضافة الرمز
        self.initialize_driver()  # تم نقل هذا السطر ليكون بعد تهيئة الخصائص
    def create_proxy_auth_extension(self):
        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            }
        }
        """

        background_js = f"""
        var config = {{
                mode: "fixed_servers",
                rules: {{
                singleProxy: {{
                    scheme: "http",
                    host: "{self.proxy.split(':')[0]}",
                    port: parseInt({self.proxy.split(':')[1]})
                }},
                bypassList: ["localhost"]
                }}
            }};

        chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

        chrome.webRequest.onAuthRequired.addListener(
                function(details) {{
                    return {{
                        authCredentials: {{
                            username: "{self.username_proxy}",
                            password: "{self.password_proxy}"
                        }}
                    }};
                }},
                {{urls: ["<all_urls>"]}},
                ['blocking']
        );
        """

        # Updated directory path
        ext_dir = "C:\\Program Files\\Google\\Chrome\\Application\\119.0.6045.160\\src\\temp_proxy_extension_{}".format(self.profile_id)
        
        # Check and create directory with administrative privileges if necessary
        if not os.path.exists(ext_dir):
            try:
                os.makedirs(ext_dir, exist_ok=True)
            except PermissionError:
                raise PermissionError("Administrative privileges required to create directory at {}".format(ext_dir))

        manifest_path = os.path.join(ext_dir, 'manifest.json')
        with open(manifest_path, 'w') as f:
            f.write(manifest_json)

        background_path = os.path.join(ext_dir, 'background.js')
        with open(background_path, 'w') as f:
            f.write(background_js)
        return ext_dir
    
    def clear_profile_data(self):
        profile_dir = f"C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data\\{self.profile_id}"
        try:
            if os.path.exists(profile_dir):
                shutil.rmtree(profile_dir)
                print(f"Profile data cleared for profile: {self.profile_id}")
            else:
                print(f"No profile data found for profile: {self.profile_id}")
        except Exception as e:
            print(f"Error clearing profile data: {e}")
    def initialize_driver(self):
        vpn1 = os.path.join("src","Windscribe")
        # self.clear_profile_data()
        global driver_lock
        with driver_lock:
            options = uc.ChromeOptions()
            options.add_argument("--enable-extensions")
            options.add_argument("--allow-in-incognito")
            options.add_argument(f"--load-extension={vpn1}")
            if self.use_proxy and self.proxy:
                proxy_extension_dir = self.create_proxy_auth_extension()
                print(proxy_extension_dir)
                options.add_argument(f"--load-extension={proxy_extension_dir}")
            options.add_argument(f"--user-data-dir=C:\\Users\\HP\\AppData\\Local\\Google\\Chrome\\User Data\\{self.profile_id}")
            if self.option == "--headless":
                options.add_argument("--headless")
            self.driver = uc.Chrome(options=options, use_subprocess=True)

    def open_url(self, url):
        try:
            self.driver.get(url)
            sleep(15)
            print(self.token)
            self.driver.add_cookie({"name": "auth-token", "value": self.token})
            # if self.use_proxy:
            #     token = self.get_token()
            #     print(token)
            #     self.driver.add_cookie({"name": "auth-token", "value": token})
            # else:
            #     cookie = self.set_x_main()
            #     self.driver.add_cookie(cookie)

            # تحديث الصفحة مرة واحدة فقط بعد إضافة الكوكي
            self.driver.refresh()
            sleep(2)  # يمكنك ضبط وقت الانتظار حسب الحاجة

        except Exception as e:
            print(f"Error in open_url: {e}")
    def set_x_main(self):
        cookie = {"name": "auth-token", "value": "k4jjqecvjshhm0hk20spjvlbpq0vpx"}
        return cookie
    def load_comments_from_json(self):
        # قراءة الملف JSON وتحميل البيانات
        with open(self.json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        comments = [item['comment'] for item in data]  # استخراج النصوص
        random.shuffle(comments)  # خلط النصوص بشكل عشوائي
        return comments
    def reload_page_if_dialog_present(self):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[role="dialog"]')))
            print("Dialog detected, reloading page.")
            self.driver.refresh()
        except TimeoutException:
            print("No dialog detected.")
    def send_chat_message(self, message):
        try:
            wait = WebDriverWait(self.driver, 5)
            chat_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-a-target="chat-input"]')))
            chat_input.send_keys(message)
            chat_input.send_keys(Keys.ENTER)
            print(f"Message sent: {message}")
        except NoSuchElementException:
            print("Chat input element not found.")
        except Exception as e:
            print(f"Error while sending message: {e}")
    def follow_if_button_found(self):
        try:
            wait = WebDriverWait(self.driver, 5)
            follow_button = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-a-target="follow-button"]')))
            follow_button.click()
            sleep(5) # انتظار لمدة 5 ثواني بعد النقر
            print("Follow button clicked.")
        except TimeoutException:
            print("Follow button not found, continuing.")
        except Exception as e:
            print(f"Error while clicking follow button: {e}")
    def start(self):
        try:
            url = "https://www.twitch.tv/noubi_elaziz"
            self.open_url(url)
            for comment in cycle(self.comments):
                self.send_chat_message(comment)
                sleep(random.randint(30, 180))
        except Exception as e:
            print(f"An error occurred in start method: {e}")



