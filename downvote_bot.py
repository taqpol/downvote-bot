from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import random
import datetime
import pytz
from dateutil.parser import parse

chromedriver_autoinstaller.install()

driver = webdriver.Chrome()

username_field = input('enter your username: ')
password_field = input('enter your password: ')

driver.get('https://old.reddit.com/login')

try:
    driver.find_element(By.ID, 'user_login').send_keys(username_field)
    driver.find_element(By.ID, 'passwd_login').send_keys(password_field + Keys.ENTER)
except Exception as ex:
    print(f"Error: {ex}")
    driver.quit()
else:
    time.sleep(5)

file_name = "names.txt"

try:
    with open(file_name) as file:
        names = [line.rstrip('\n') for line in file]
except FileNotFoundError:
    print('there was a problem locating the file')
    driver.quit()

aware_time_now = pytz.utc.localize(datetime.datetime.now())

for name in names:
    driver.get('https://old.reddit.com/user/{}'.format(name))
    print('downvoting {}...'.format(name))
    print('starting karma: {}'.format(driver.find_element(By.CLASS_NAME, 'comment-karma').text))

    try:
        comments = driver.find_elements(By.CLASS_NAME, 'thing')
        downvote_arrows = [comment.find_elements(By.CLASS_NAME, 'arrow')[1] for comment in comments]
        timestamps = [comment.find_element(By.TAG_NAME, 'time') for comment in comments]
    except:
        driver.quit()

    if not len(timestamps):
        continue
    if (aware_time_now - parse(timestamps[0].get_attribute('datetime'))).days > 2:
        continue
    for downvote_button, timestamp in zip(downvote_arrows, timestamps):
        if (aware_time_now - parse(timestamp.get_attribute('datetime'))).days < 2:
            if 'downmod' not in downvote_button.get_attribute('class'):
                downvote_button.click()
                pause_time = random.randint(90,120)
                print('downvoted at {}. pausing for {} seconds...'.format(datetime.datetime.now(), pause_time))
                time.sleep(pause_time)
            else:
                pass
        else:
            # driver.refresh()
            # time.sleep(3)
            # print('ending karma after series: {}'.format(driver.find_element_by_class_name('comment-karma').text))
            continue

    if (aware_time_now - parse(timestamps[-1].get_attribute('datetime'))).days < 2:
        try:
            next_button = driver.find_element(By.PARTIAL_LINK_TEXT, 'next')
        except:
            continue
        else:
            # driver.refresh()
            # time.sleep(3)
            # next_button = driver.find_element_by_partial_link_text('next')
            # print('ending karma after series: {}'.format(driver.find_element_by_class_name('comment-karma').text))
            next_button.click()
    else:
        continue

driver.quit()