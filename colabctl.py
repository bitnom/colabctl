import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle
import time


def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            continue


def exists_by_text(driver, text):
    driver.implicitly_wait(0)
    try:
        driver.find_element_by_xpath("//*[contains(text(), '"+str(text)+"')]")
    except NoSuchElementException:
        driver.implicitly_wait(30)
        return False
    driver.implicitly_wait(30)
    return True


def user_logged_in(driver):
    try:
        driver.find_element_by_xpath('//*[@id="file-type"]')
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(30)
    return True

fork = sys.argv[1]
timeout = int(sys.argv[2])
colab_url = sys.argv[3]

chrome_options = Options()
#chrome_options.add_argument('--headless') # uncomment for headless mode
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("user-data-dir=profile") # left for debugging
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver', options=chrome_options)

wd.get(colab_url)
try:
    for cookie in pickle.load(open("gCookies.pkl", "rb")):
        wd.add_cookie(cookie)
except Exception:
    pass
wd.get(colab_url)

if exists_by_text(wd, "Sign in"):
    print("No auth cookie detected. Please login to Google.")
    wd.close()
    wd.quit()
    chrome_options_gui = Options()
    chrome_options_gui.add_argument('--no-sandbox')
    #chrome_options.add_argument("user-data-dir=profile") # left for debugging
    chrome_options_gui.add_argument('--disable-infobars')
    wd = webdriver.Chrome('chromedriver', options=chrome_options_gui)
    wd.get("https://accounts.google.com/signin")
    while not exists_by_text(wd, "Welcome,"):
        pass
    print("Login detected. Saving cookie & restarting connection.")
    pickle.dump(wd.get_cookies(), open("gCookies.pkl", "wb"))
    wd.close()
    wd.quit()
    wd = webdriver.Chrome('chromedriver', options=chrome_options)

print("Now ready for business.") # for debugging
running = False
while not exists_by_text(wd, "Sign in"):
    if exists_by_text(wd, "Runtime disconnected"):
        try:
            wd.find_element_by_xpath('//*[@id="ok"]').click()
        except NoSuchElementException:
            pass
    if exists_by_text(wd, "Notebook loading error"):
        wd.get(colab_url)
    try:
        wd.find_element_by_xpath('/html/body/div[7]/div[1]/div[2]/colab-connect-button/colab-toolbar-button[1]/paper-button/iron-icon')
        if not running:
            wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.F9)
            running = True
            sleep(2)
    except NoSuchElementException:
        pass
    if running:
        if exists_by_text(wd, fork):
            running = False
            print("Completion string found. Waiting for next cycle.")
            sleep(timeout)
        else:
            try:
                actions = ActionChains(wd)
                actions.send_keys(Keys.SPACE).perform()
            except Exception:
                pass
