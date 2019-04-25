import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import validators


def sleep(seconds):
    for i in range(seconds):
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            continue


def exists_by_text2(driver, text):
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(), '"+str(text)+"')]")))
    except Exception:
        return False
    return True


def exists_by_text(driver, text):
    driver.implicitly_wait(2)
    try:
        driver.find_element_by_xpath("//*[contains(text(), '"+str(text)+"')]")
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(5)
    return True


def user_logged_in(driver):
    try:
        driver.find_element_by_xpath('//*[@id="file-type"]')
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(5)
    return True


def wait_for_xpath(driver, x):
    while True:
        try:
            driver.find_element_by_xpath(x)
            return True
        except:
            time.sleep(0.1)
            pass


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 0.5
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def file_to_list(filename):
    colabs = []
    for line in open(filename):
        if validators.url(line):
            colabs.append(line)
    return colabs
    

fork = sys.argv[1]
timeout = int(sys.argv[2])
colab_urls = file_to_list('notebooks.csv')

if len(colab_urls) > 0 and validators.url(colab_urls[0]):
    colab_1 = colab_urls[0]
else:
    raise Exception('No notebooks')

chrome_options = Options()
#chrome_options.add_argument('--headless') # uncomment for headless mode
chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument("user-data-dir=profile") # left for debugging
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('chromedriver', options=chrome_options)

wd.get(colab_1)
try:
    for cookie in pickle.load(open("gCookies.pkl", "rb")):
        wd.add_cookie(cookie)
except Exception:
    pass
wd.get(colab_1)

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
    wait_for_xpath(wd, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/c-wiz/div/div[4]/div/div/header/div[2]')
    print("Login detected. Saving cookie & restarting connection.")
    pickle.dump(wd.get_cookies(), open("gCookies.pkl", "wb"))
    wd.close()
    wd.quit()
    wd = webdriver.Chrome('chromedriver', options=chrome_options)

for colab_url in colab_urls:
    complete = False
    wd.get(colab_url)
    print("Logged in.") # for debugging
    running = False
    wait_for_xpath(wd, '//*[@id="file-menu-button"]/div/div/div[1]')
    print('Notebook loaded.')

    while not exists_by_text(wd, "Sign in"):
        if exists_by_text(wd, "Runtime disconnected"):
            try:
                wd.find_element_by_xpath('//*[@id="ok"]').click()
            except NoSuchElementException:
                pass
        if exists_by_text2(wd, "Notebook loading error"):
            wd.get(colab_url)
        try:
            wd.find_element_by_xpath('//*[@id="file-menu-button"]/div/div/div[1]')
            if not running:
                wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.SHIFT + "q")
                wd.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.F9)
                running = True
        except NoSuchElementException:
            pass
        if running:
            try:
                wd.find_element_by_css_selector('.notebook-content-background').click()
                #actions = ActionChains(wd)
                #actions.send_keys(Keys.SPACE).perform()
                scroll_to_bottom(wd)
                print("performed scroll")
            except:
                pass
            for frame in wd.find_elements_by_tag_name('iframe'):
                wd.switch_to.frame(frame)
                for output in wd.find_elements_by_tag_name('pre'):
                    if fork in output.text:
                        running = False
                        complete = True
                        print("Completion string found. Waiting for next cycle.")
                        break
                wd.switch_to.default_content()
                if complete:
                    break
            if complete:
                break
    sleep(timeout)

